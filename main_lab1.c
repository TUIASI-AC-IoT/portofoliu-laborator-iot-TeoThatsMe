#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"
#define GPIO_OUTPUT_IO 4
#define GPIO_OUTPUT_PIN_SEL (1ULL<<GPIO_OUTPUT_IO)
#define GPIO_INPUT_IO 2
#define GPIO_INPUT_PIN_SEL (1ULL<<GPIO_INPUT_IO)

static QueueHandle_t gpio_evt_queue = NULL;
static int pressed_button_cnt = 0;
static int prev_state = 0;
void clipocesc()
{
    gpio_set_level(GPIO_OUTPUT_IO, 0);
    vTaskDelay(1000 / portTICK_PERIOD_MS);
    gpio_set_level(GPIO_OUTPUT_IO, 1);
    vTaskDelay(500 / portTICK_PERIOD_MS);
    gpio_set_level(GPIO_OUTPUT_IO, 0);
    vTaskDelay(250 / portTICK_PERIOD_MS);
    gpio_set_level(GPIO_OUTPUT_IO, 1);
    vTaskDelay(750 / portTICK_PERIOD_MS); 
}





static void IRAM_ATTR gpio_isr_handler(void* arg)
{
    uint32_t gpio_num = (uint32_t) arg;
    xQueueSendFromISR(gpio_evt_queue, &gpio_num, NULL);
}

static void gpio_task_example(void* arg)
{
    uint32_t io_num;
    for (;;) {
        if (xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
            pressed_button_cnt+=1;
            printf("Buton apasat de %d ori", pressed_button_cnt);
        }
        
    }
}

static void gpio_task_example_ex3(void* arg)
{
    uint32_t io_num;
    for (;;) {
        if (xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
            prev_state = prev_state == 0;
            if(prev_state) {
                clipocesc();
            }
            else {
                gpio_set_level(GPIO_OUTPUT_IO, 1);
            }
        }
    }
}


void app_main() {
    //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);


    io_conf.intr_type = GPIO_INTR_POSEDGE;
    io_conf.pin_bit_mask = GPIO_INPUT_PIN_SEL;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_up_en = 1;


    gpio_config(&io_conf);


    gpio_set_intr_type(GPIO_INPUT_IO, GPIO_INTR_POSEDGE);
    gpio_evt_queue = xQueueCreate(10, sizeof(uint32_t));
    





    int cnt = 0;
    int exercitiu = 3;
    if(exercitiu == 1) {
        while(1) {
            printf("cnt: %d\n", cnt++);
            clipocesc();
        }
    }
    else if(exercitiu == 2){
        xTaskCreate(gpio_task_example, "gpio_task_example", 2048, NULL, 10, NULL);
        gpio_install_isr_service(0);
        gpio_isr_handler_add(GPIO_INPUT_IO, gpio_isr_handler, (void*) GPIO_INPUT_IO);
        
        while(1) {
            printf("curr_cnt: %d\n", pressed_button_cnt);
            vTaskDelay(1000 / portTICK_PERIOD_MS);
        }
    }
    else if(exercitiu == 3){
        xTaskCreate(gpio_task_example_ex3, "gpio_task_example_ex3", 2048, NULL, 10, NULL);
        gpio_install_isr_service(0);
        gpio_isr_handler_add(GPIO_INPUT_IO, gpio_isr_handler, (void*) GPIO_INPUT_IO);
        while(1) {
            vTaskDelay(1000 / portTICK_PERIOD_MS);
        }
    }
}