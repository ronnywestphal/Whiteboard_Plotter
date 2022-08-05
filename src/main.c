#include "gd32vf103.h"
#include "canFunctions.h"
#include "shapeFunctions.h"
#include "delay.h"
#include <math.h>

#define CAN_NO_MESSAGE 0xFFF

int main(void)
{
    int P_coordinates[8];

    short int pointerX=0;             // startläget på plottern ugår från vad dessa värden är satta till.
    short int pointerY=0;             

    can_receive_message_struct can_message;
    can_struct_para_init(CAN_RX_MESSAGE_STRUCT, &can_message);

    can_rx_buffer_t receive_buffer;
    can_buffer_init(&receive_buffer);
    can_networking_init();
    
    init_ADC();
   
    /*initialize pins*/
    rcu_periph_clock_enable(RCU_GPIOA);
    rcu_periph_clock_enable(RCU_GPIOB);
    rcu_periph_clock_enable(RCU_AF);

    gpio_init(GPIOA, GPIO_MODE_AF_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_1);   // PWM, timer channel 4 pin


    gpio_init(GPIOB, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_12 | GPIO_PIN_13 | GPIO_PIN_14 | GPIO_PIN_15);
    gpio_init(GPIOB, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_8 | GPIO_PIN_9 | GPIO_PIN_10 | GPIO_PIN_11);

    gpio_port_write(GPIOB, gpio_output_port_get(GPIOB) & 0xF0FF);

    gpio_init(GPIOA, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_4);
    gpio_init(GPIOA, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_3);
    gpio_init(GPIOB, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_1);
    gpio_init(GPIOB, GPIO_MODE_OUT_PP, GPIO_OSPEED_50MHZ, GPIO_PIN_0);

    init_PWM_example(); 

    while(1){

        /* Start ADC conversion */
        adc_software_trigger_enable(ADC0, ADC_INSERTED_CHANNEL);

        /* Check receive buffer */
        can_message = can_buffer_pop(&receive_buffer);

        /* Check if there was a new message, if so execute corresponding functions */
        if(can_message.rx_sfid != CAN_NO_MESSAGE){
            CAN_receive_message_execute(can_message,P_coordinates, &pointerX,&pointerY);       
        } 
        
    }
    
}
