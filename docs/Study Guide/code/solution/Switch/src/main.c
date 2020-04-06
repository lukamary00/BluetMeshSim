/**
 * On/Off Switch Node - behaviour predominantly based on the Bluetooth mesh Generic OnOff Client Model
 * 
 * Coded for and tested with nRF52840 DK board
 * 
 **/

#include <misc/printk.h>
#include <gpio.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/mesh.h>
#include <settings/settings.h>
#include <bluetooth/mesh/proxy.h>

// GPIO for the buttons
#define PORT1 SW0_GPIO_CONTROLLER
#define PORT2 SW1_GPIO_CONTROLLER
#define PORT3 SW2_GPIO_CONTROLLER
#define PORT4 SW3_GPIO_CONTROLLER
#define BUTTON1 SW0_GPIO_PIN
#define BUTTON2 SW1_GPIO_PIN
#define BUTTON3 SW2_GPIO_PIN
#define BUTTON4 SW3_GPIO_PIN

#ifdef SW0_GPIO_FLAGS
#define EDGE    (SW0_GPIO_FLAGS | GPIO_INT_EDGE)
#else
#define EDGE    (GPIO_INT_EDGE | GPIO_INT_ACTIVE_LOW)
#endif

#ifndef SW0_GPIO_FLAGS
#ifdef SW0_GPIO_PIN_PUD
#define SW0_GPIO_FLAGS SW0_GPIO_PIN_PUD
#else
#define SW0_GPIO_FLAGS 0
#endif
#endif
#define PULL_UP SW0_GPIO_FLAGS

#define BUTTON_DEBOUNCE_DELAY_MS 250

static u32_t btn_time[4] = { 0,0,0,0};
static u32_t btn_last_time[4] = { 0,0,0,0};

static struct gpio_callback gpio_btn1_cb;
static struct gpio_callback gpio_btn2_cb;
static struct gpio_callback gpio_btn3_cb;
static struct gpio_callback gpio_btn4_cb;

// GPIO for LED 0
struct device *gpio_led_port;
#define LED_PORT LED0_GPIO_CONTROLLER
#define LED0 LED0_GPIO_PIN

// for use with k_work_submit which we use to handle button presses in a background thread to avoid holding onto an IRQ for too long
static struct k_work button1_work;
static struct k_work button2_work;
static struct k_work button3_work;
static struct k_work button4_work;

static const uint8_t dev_uuid[16] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x00 };


static u8_t onoff_tid;
static u8_t hsl_tid;

void ledOn(void) {
	gpio_pin_write(gpio_led_port, LED0, 0);
}

void ledOff(void) {
	gpio_pin_write(gpio_led_port, LED0, 1);
}

static void attention_on(struct bt_mesh_model *model)
{
	printk("attention_on()\n");
	ledOn();
}

static void attention_off(struct bt_mesh_model *model)
{
	printk("attention_off()\n");
	ledOff();
}

static const struct bt_mesh_health_srv_cb health_srv_cb = {
	.attn_on = attention_on,
	.attn_off = attention_off,
};

static int provisioning_output_pin(bt_mesh_output_action_t action, u32_t number) {
	printk("OOB Number: %04d\n", number);
	return 0;
}

static void provisioning_complete(u16_t net_idx, u16_t addr) {
    printk("Provisioning completed\n");
}

static void provisioning_reset(void)
{
	bt_mesh_prov_enable(BT_MESH_PROV_ADV | BT_MESH_PROV_GATT);
}

// provisioning properties and capabilities
static const struct bt_mesh_prov prov = {
	.uuid = dev_uuid,
	.output_size = 4,
	.output_actions = BT_MESH_DISPLAY_NUMBER,
	.output_number = provisioning_output_pin,
	.complete = provisioning_complete,
	.reset = provisioning_reset,
};

// -------------------------------------------------------------------------------------------------------
// Configuration Server
// --------------------
static struct bt_mesh_cfg_srv cfg_srv = {
		.relay = BT_MESH_RELAY_DISABLED,
		.beacon = BT_MESH_BEACON_DISABLED,
		.frnd = BT_MESH_FRIEND_NOT_SUPPORTED,
		.gatt_proxy = BT_MESH_GATT_PROXY_ENABLED,
		.default_ttl = 7,
		/* 3 transmissions with 20ms interval */
		.net_transmit = BT_MESH_TRANSMIT(2, 20),
};


// -------------------------------------------------------------------------------------------------------
// Health Server
// -------------
BT_MESH_HEALTH_PUB_DEFINE(health_pub, 0);
static struct bt_mesh_health_srv health_srv = {
	.cb = &health_srv_cb,
};

// -------------------------------------------------------------------------------------------------------
// Generic OnOff Client Model
// --------------------------

u8_t onoff[] = {
	0,
	1};

// handler functions for this model's RX messages

static void generic_onoff_status(struct bt_mesh_model *model,struct bt_mesh_msg_ctx *ctx,struct net_buf_simple *buf)
{
	u8_t onoff_state = net_buf_simple_pull_u8(buf);
	printk("generic_onoff_status onoff=%d\n",onoff_state);   
}

// generic on off client - message types defined by this model

#define BT_MESH_MODEL_OP_GENERIC_ONOFF_GET	      BT_MESH_MODEL_OP_2(0x82, 0x01)
#define BT_MESH_MODEL_OP_GENERIC_ONOFF_SET	      BT_MESH_MODEL_OP_2(0x82, 0x02)
#define BT_MESH_MODEL_OP_GENERIC_ONOFF_SET_UNACK  BT_MESH_MODEL_OP_2(0x82, 0x03)
#define BT_MESH_MODEL_OP_GENERIC_ONOFF_STATUS     BT_MESH_MODEL_OP_2(0x82, 0x04)

static const struct bt_mesh_model_op gen_onoff_cli_op[] = {
		{BT_MESH_MODEL_OP_GENERIC_ONOFF_STATUS, 1, generic_onoff_status},
		BT_MESH_MODEL_OP_END,
};

// -------------------------------------------------------------------------------------------------------
// Light HSL Client Model
// ----------------------

/*
BLACK   : HSL(    0,    0,    0) = RGB(0,0,0)

RED     : HSL(    0,65535,32767) = RGB(255,0,0)

GREEN   : HSL(21845,65535,32767) = RGB(0,255,0)

BLUE    : HSL(43690,65535,32767) = RGB(0,0,255)

YELLOW  : HSL(10922,65535,32767) = RGB(255,255,0)

MAGENTA : HSL(54613,65535,32767) = RGB(255,0,255)

CYAN    : HSL(32768,65535,32767) = RGB(0,255,255)

WHITE   : HSL(    0,    0,65535) = RGB(255,255,255)
*/

#define NUMBER_OF_COLOURS 8

u16_t hsl[NUMBER_OF_COLOURS][3] = {
	{ 0x0000, 0x0000, 0x0000 }, // black
	{ 0x0000, 0xFFFF, 0x7FFF }, // red 
	{ 0x5555, 0xFFFF, 0x7FFF }, // green
	{ 0xAAAA, 0xFFFF, 0x7FFF }, // blue
	{ 0x2AAA, 0xFFFF, 0x7FFF }, // yellow
	{ 0xD555, 0xFFFF, 0x7FFF }, // magenta
	{ 0x7FFF, 0xFFFF, 0x7FFF }, // cyan
	{ 0x0000, 0x0000, 0xFFFF }  // white
};

u8_t current_hsl_inx = 1;

// message types defined by this model.
#define BT_MESH_MODEL_OP_LIGHT_HSL_SET_UNACK	BT_MESH_MODEL_OP_2(0x82, 0x77)

// -------------------------------------------------------------------------------------------------------
// Composition
// -----------

BT_MESH_MODEL_PUB_DEFINE(gen_onoff_cli, NULL, 2);
BT_MESH_MODEL_PUB_DEFINE(light_hsl_cli, NULL, 2);

static struct bt_mesh_model sig_models[] = {
				BT_MESH_MODEL_CFG_SRV(&cfg_srv),
				BT_MESH_MODEL_HEALTH_SRV(&health_srv, &health_pub),
				BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_ONOFF_CLI, gen_onoff_cli_op, &gen_onoff_cli, &onoff[0]),
				BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_HSL_CLI, NULL, &light_hsl_cli, &hsl[0]),
};

// node contains elements. Note that BT_MESH_MODEL_NONE means "none of this type" and here means "no vendor models"
static struct bt_mesh_elem elements[] = {
				BT_MESH_ELEM(0, sig_models, BT_MESH_MODEL_NONE),
};

// node
static const struct bt_mesh_comp comp = {
				.cid = 0xFFFF,
				.elem = elements,
				.elem_count = ARRAY_SIZE(elements),
};


// Generic OnOff Client - TX message producer functions
// -----------------------------------------------------------

int genericOnOffGet() 
{
	printk("genericOnOffGet\n");
    int err;
    struct bt_mesh_model *model = &sig_models[2];
	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		printk("No publish address associated with the generic on off client model - add one with a configuration app like nRF Mesh\n");
		return -1;
	}     
	struct net_buf_simple *msg = model->pub->msg;

	bt_mesh_model_msg_init(msg,	BT_MESH_MODEL_OP_GENERIC_ONOFF_GET);
	printk("publishing get on off message\n");
	err = bt_mesh_model_publish(model);
	if (err) {
		printk("bt_mesh_model_publish err %d\n", err);
	}

	return err;
}

int sendGenOnOffSet(u8_t on_or_off, u16_t message_type) 
{
    int err;
    struct bt_mesh_model *model = &sig_models[2];
	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		printk("No publish address associated with the generic on off client model - add one with a configuration app like nRF Mesh\n");
		return -1;
	}     
	struct net_buf_simple *msg = model->pub->msg;

	bt_mesh_model_msg_init(msg,	message_type);
	net_buf_simple_add_u8(msg, on_or_off);
	net_buf_simple_add_u8(msg, onoff_tid);
	onoff_tid++;
	printk("publishing set on off state=0x%02x\n",on_or_off);
	err = bt_mesh_model_publish(model);
	if (err) {
		printk("bt_mesh_model_publish err %d\n", err);
	}

	return err;
}

void genericOnOffSetUnAck(u8_t on_or_off) 
{
	if (sendGenOnOffSet(on_or_off, BT_MESH_MODEL_OP_GENERIC_ONOFF_SET_UNACK))
	{
		printk("Unable to send generic onoff set unack message\n");
	} else {
	    printk("onoff set unack message %d sent\n",on_or_off);
	}
}


void genericOnOffSet(u8_t on_or_off) 
{
	if (sendGenOnOffSet(on_or_off, BT_MESH_MODEL_OP_GENERIC_ONOFF_SET))
	{
		printk("Unable to send generic onoff set message\n");
	} else {
		printk("onoff set message %d sent\n",on_or_off);
	}
}


// Light HSL Client - TX message producer functions
// -----------------------------------------------------------

int sendLightHslSet(u16_t message_type) 
{
    int err;
    struct bt_mesh_model *model = &sig_models[3];
	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		printk("No publish address associated with the light HSL client model - add one with a configuration app like nRF Mesh\n");
		return -1;
	}     
	struct net_buf_simple *msg = model->pub->msg;

	bt_mesh_model_msg_init(msg,	message_type);
	net_buf_simple_add_le16(msg, hsl[current_hsl_inx][2]); // Yes, index value 2 is correct - ordering of params is Lightness, Hue, Saturation
	net_buf_simple_add_le16(msg, hsl[current_hsl_inx][0]);
	net_buf_simple_add_le16(msg, hsl[current_hsl_inx][1]);
	net_buf_simple_add_u8(msg, hsl_tid);
	hsl_tid++;
	printk("publishing light HSL set message\n");
	err = bt_mesh_model_publish(model);
	if (err) {
		printk("bt_mesh_model_publish err %d\n", err);
	} else {
		current_hsl_inx++;
		if (current_hsl_inx == NUMBER_OF_COLOURS) {
			current_hsl_inx = 0;
		}
	}

	return err;
}

void lightHslSetUnAck() 
{
	if (sendLightHslSet(BT_MESH_MODEL_OP_LIGHT_HSL_SET_UNACK))
	{
		printk("Unable to send light HSL set unack message\n");
	}
}

// Buttons
// -------
void button1_work_handler(struct k_work *work)
{
    genericOnOffSetUnAck(onoff[1]);
	// genericOnOffSet(onoff[1]);
}

void button2_work_handler(struct k_work *work)
{
    genericOnOffSetUnAck(onoff[0]);
	// genericOnOffSet(onoff[0]);
}

void button3_work_handler(struct k_work *work)
{	
 	genericOnOffGet();
}

void button4_work_handler(struct k_work *work)
{
	lightHslSetUnAck();
}

bool debounce(int btn_inx) {
	bool ignore = false;
	btn_time[btn_inx] = k_uptime_get_32();
	if (btn_time[btn_inx] < (btn_last_time[btn_inx] + BUTTON_DEBOUNCE_DELAY_MS)) {
		ignore = true;
	} else {
		ignore = false;
	}
	btn_last_time[btn_inx] = btn_time[btn_inx];
	return ignore;
}

void button_1_pressed(struct device *gpiob, struct gpio_callback *cb,
											u32_t pins)
{
	// printk("Button 1 pressed at %d\n", k_cycle_get_32());

    if (!debounce(0)) {
	  k_work_submit(&button1_work);
	}
}

void button_2_pressed(struct device *gpiob, struct gpio_callback *cb,
											u32_t pins)
{
	// printk("Button 2 pressed at %d\n", k_cycle_get_32());
    if (!debounce(1)) {
	  k_work_submit(&button2_work);
	}
}

void button_3_pressed(struct device *gpiob, struct gpio_callback *cb,
											u32_t pins)
{
	// printk("Button 3 pressed at %d\n", k_cycle_get_32());
    if (!debounce(2)) {
	  k_work_submit(&button3_work);
	}
}

void button_4_pressed(struct device *gpiob, struct gpio_callback *cb,
											u32_t pins)
{
	// printk("Button 4 pressed at %d\n", k_cycle_get_32());
    if (!debounce(3)) {
	  k_work_submit(&button4_work);
	}
}

// -------------------------------------------------------------------------------------------------------
// LED
// -------

void configureLED(void)
{
	printk("configureLED\n");

	gpio_led_port = device_get_binding(LED_PORT);
	if (!gpio_led_port)
	{
		printk("error obtaining LED port\n");
		return;
	}


	// LED 0
	gpio_pin_configure(gpio_led_port, LED0, GPIO_DIR_OUT);
	ledOff();
}


// -------------------------------------------------------------------------------------------------------
// Buttons
// -------

void configureButtons(void)
{
	printk("configureButtons\n");

	struct device *gpio_port1;
	struct device *gpio_port2;
	struct device *gpio_port3;
	struct device *gpio_port4;

	gpio_port1 = device_get_binding(PORT1);
	if (!gpio_port1)
	{
		printk("error obtaining port 1\n");
		return;
	}

	gpio_port2 = device_get_binding(PORT2);
	if (!gpio_port2)
	{
		printk("error obtaining port 2\n");
		return;
	}

	gpio_port3 = device_get_binding(PORT3);
	if (!gpio_port3)
	{
		printk("error obtaining port 3\n");
		return;
	}

	gpio_port4 = device_get_binding(PORT4);
	if (!gpio_port4)
	{
		printk("error obtaining port 4\n");
		return;
	}

	// Button 1
	k_work_init(&button1_work, button1_work_handler);
	gpio_pin_configure(gpio_port1, BUTTON1, GPIO_DIR_IN | GPIO_INT |  PULL_UP | EDGE);
	gpio_init_callback(&gpio_btn1_cb, button_1_pressed, BIT(BUTTON1));
	gpio_add_callback(gpio_port1, &gpio_btn1_cb);
	gpio_pin_enable_callback(gpio_port1, BUTTON1);

	// Button 2
	k_work_init(&button2_work, button2_work_handler);
	gpio_pin_configure(gpio_port2, BUTTON2, GPIO_DIR_IN | GPIO_INT | PULL_UP | EDGE);
	gpio_init_callback(&gpio_btn2_cb, button_2_pressed, BIT(BUTTON2));
	gpio_add_callback(gpio_port2, &gpio_btn2_cb);
	gpio_pin_enable_callback(gpio_port2, BUTTON2);

	// Button 3
	k_work_init(&button3_work, button3_work_handler);
	gpio_pin_configure(gpio_port3, BUTTON3, GPIO_DIR_IN | GPIO_INT | PULL_UP | EDGE);
	gpio_init_callback(&gpio_btn3_cb, button_3_pressed, BIT(BUTTON3));
	gpio_add_callback(gpio_port3, &gpio_btn3_cb);
	gpio_pin_enable_callback(gpio_port3, BUTTON3);

	// Button 4
	k_work_init(&button4_work, button4_work_handler);
	gpio_pin_configure(gpio_port4, BUTTON4, GPIO_DIR_IN | GPIO_INT | PULL_UP | EDGE);
	gpio_init_callback(&gpio_btn4_cb, button_4_pressed, BIT(BUTTON4));
	gpio_add_callback(gpio_port4, &gpio_btn4_cb);
	gpio_pin_enable_callback(gpio_port4, BUTTON4);
}

static void bt_ready(int err)
{
	if (err)
	{
			printk("bt_enable init failed with err %d\n", err);
			return;
	}

	printk("Bluetooth initialised OK\n");

	// prov is a bt_mesh_prov struct and is declared in provisioning.c
	err = bt_mesh_init(&prov, &comp);
	if (err)
	{
			printk("bt_mesh_init failed with err %d\n", err);
			return;
	}

	printk("Mesh initialised OK\n");

	if (IS_ENABLED(CONFIG_SETTINGS)) {
		settings_load();
	    printk("Settings loaded\n");
	}

    if (!bt_mesh_is_provisioned()) {
    	printk("Node has not been provisioned - beaconing\n");
		bt_mesh_prov_enable(BT_MESH_PROV_ADV | BT_MESH_PROV_GATT);
	} else {
    	printk("Node has already been provisioned\n");
	}

}


void main(void)
{
	int err;
	printk("switch\n");

	onoff_tid = 0;
	hsl_tid = 0;

	configureButtons();

	configureLED();

	err = bt_enable(bt_ready);
	if (err)
	{
			printk("bt_enable failed with err %d\n", err);
	}
}
