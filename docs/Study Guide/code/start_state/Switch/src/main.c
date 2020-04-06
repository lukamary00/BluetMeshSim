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

// for debouncing the four buttons
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


static const struct bt_mesh_health_srv_cb health_srv_cb = {
};

// provisioning properties and capabilities


// -------------------------------------------------------------------------------------------------------
// Configuration Server
// --------------------


// -------------------------------------------------------------------------------------------------------
// Health Server
// -------------


// -------------------------------------------------------------------------------------------------------
// Generic OnOff Client Model
// --------------------------

u8_t onoff[] = {
	0,
	1};

// generic on off client - handler functions for this model's RX messages


// generic on off client - message types defined by this model.


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


// Generic OnOff Client - TX message producer functions
// -----------------------------------------------------------

// Light HSL Client - TX message producer functions
// -----------------------------------------------------------


// Buttons
// -------
void button1_work_handler(struct k_work *work)
{
}

void button2_work_handler(struct k_work *work)
{
}

void button3_work_handler(struct k_work *work)
{	
}

void button4_work_handler(struct k_work *work)
{
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


void main(void)
{
	int err;
	printk("switch\n");

	onoff_tid = 0;
	hsl_tid = 0;

	configureButtons();

	configureLED();

}
