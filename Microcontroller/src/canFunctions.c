#include "gd32vf103.h"
#include "canFunctions.h"
#include "shapeFunctions.h"

#define CAN_RECEIVE_BUFFER_SIZE 32
#define CAN_NO_MESSAGE 0xFFF


// PWM 
#define PWMC1_PORT     GPIOA
#define PWMC1_PIN      GPIO_PIN_1
#define PWM_CHANNEL    


/* This is a fix for an earlier version of the API which did not include this interrupt. In later version CAN_INT_FLAG_RFL1 should be used */
#define CAN_RX_FIFO1_NOT_EMPTY (((uint32_t)(RFIFO1_REG_OFFSET) << 12) | ((uint32_t)(2U) << 6) | (uint32_t)(4U))


/* Some FIFO-functions for CAN messages */

const can_receive_message_struct can_no_message = {.rx_sfid = CAN_NO_MESSAGE, .rx_dlen = 0};

int can_buffer_push(can_receive_message_struct dat, can_rx_buffer_t *buf){
    if(buf->head == buf->tail) return -1; //Full
    buf->receive_message_fifo[buf->head] = dat;
    buf->head = (buf->head + 1) % CAN_RECEIVE_BUFFER_SIZE;
}

can_receive_message_struct can_buffer_pop(can_rx_buffer_t *buf){
    if((buf->head) == (buf->tail + 1) % CAN_RECEIVE_BUFFER_SIZE) return can_no_message; //Empty
    buf->tail = (buf->tail + 1) % CAN_RECEIVE_BUFFER_SIZE;
    return buf->receive_message_fifo[buf->tail];
}

void can_buffer_init(can_rx_buffer_t *buf){
    for(int i = 0; i < CAN_RECEIVE_BUFFER_SIZE; i++) can_struct_para_init(CAN_RX_MESSAGE_STRUCT, &buf->receive_message_fifo[i]);
    buf->tail = CAN_RECEIVE_BUFFER_SIZE;
    buf->head = 0;
}

/* END Compact FIFO for CAN messages */


/* This function contains all the code needed to configure the CAN-bus.
   It's a bit of a handfull but once it works right using it is fairly simple. */

void can_networking_init(void){

    /* Configuration structs used by the CAN api */
    can_parameter_struct            can_parameter;
    can_filter_parameter_struct     can_filter;

    /* Initialization of the pins used for Rx and Tx, these needs to be connected to a tranceiver */
    rcu_periph_clock_enable(RCU_GPIOB);
    rcu_periph_clock_enable(RCU_AF);
    gpio_init(GPIOB,GPIO_MODE_IPU,GPIO_OSPEED_50MHZ,GPIO_PIN_5);
    gpio_init(GPIOB,GPIO_MODE_AF_PP,GPIO_OSPEED_50MHZ,GPIO_PIN_6);
    gpio_pin_remap_config(GPIO_CAN1_REMAP,ENABLE);

    /* Both CAN1 and CAN0 needs to activate for the hardware FIFOs to work right for CAN1 */
    rcu_periph_clock_enable(RCU_CAN1);
    rcu_periph_clock_enable(RCU_CAN0);
    
    can_struct_para_init(CAN_INIT_STRUCT, &can_parameter);
    can_struct_para_init(CAN_FILTER_STRUCT, &can_filter);
    
    /* Reset CAN1 to default state */
    can_deinit(CAN1);
    
    /* These are settings for CAN module special functions, for this example, everything is off refer to the manual for more info on specifics */
    can_parameter.time_triggered = DISABLE;
    can_parameter.auto_bus_off_recovery = DISABLE;
    can_parameter.auto_wake_up = DISABLE;
    can_parameter.auto_retrans = DISABLE;
    //can_parameter.no_auto_retrans = DISABLE;
    can_parameter.rec_fifo_overwrite = DISABLE;
    can_parameter.trans_fifo_order = DISABLE;
    can_parameter.working_mode = CAN_NORMAL_MODE;

    /* These are the timing quanta for CAN timings and prescaler. These will set up a bit-time for 1Mbps*/
    can_parameter.resync_jump_width = CAN_BT_SJW_1TQ; 
    can_parameter.time_segment_1 = CAN_BT_BS1_5TQ;    
    can_parameter.time_segment_2 = CAN_BT_BS2_3TQ;    
    can_parameter.prescaler = 6;  

    /* Use the settings and initialize the CAN-bus module */
    can_init(CAN1, &can_parameter);

    /* Select a filter, no 14 is connected to CAN1 so here we use that. */
    can_filter.filter_number = 14;

    /* This could be used to filter out just the important messages
       refer to the manual for what to set. Right now it's set to accept all messages.*/    
    can_filter.filter_mode = CAN_FILTERMODE_MASK;
    can_filter.filter_bits = CAN_FILTERBITS_32BIT;
    can_filter.filter_list_high = 0x0000;
    can_filter.filter_list_low = 0x0000;
    can_filter.filter_mask_high = 0x0000;
    can_filter.filter_mask_low = 0x0000;  
    can_filter.filter_fifo_number = CAN_FIFO1;
    can_filter.filter_enable = ENABLE;
    can1_filter_start_bank(0);    
    can_filter_init(&can_filter);


    /* Setup CAN receive interrupt */
    eclic_priority_group_set(ECLIC_PRIGROUP_LEVEL2_PRIO2);
    eclic_global_interrupt_enable();
    eclic_irq_enable(CAN1_RX1_IRQn,1,0);
    can_interrupt_enable(CAN1, CAN_INTEN_RFNEIE1);
    can_interrupt_flag_clear(CAN1, CAN_RX_FIFO1_NOT_EMPTY);
    
}

/* Send CAN message routine */
void CAN_send_message(uint16_t message_id, uint8_t remote_data, uint8_t length, uint8_t *p_data){
    
    /* Initialize a blank message */
    can_trasnmit_message_struct transmit_message;
    can_struct_para_init(CAN_TX_MESSAGE_STRUCT, &transmit_message);
    
    /* Set parameters */
    transmit_message.tx_ff = CAN_FF_STANDARD;   //Standard message type. (Not extended)
    transmit_message.tx_efid = 0x0;             //Extended message ID - not used here
    transmit_message.tx_sfid = message_id;      //Standard message ID
    transmit_message.tx_dlen = length;          //How many bytes to send (min 0, max 8)
    transmit_message.tx_ft = remote_data;       //CAN_FT_REMOTE for request data, CAN_FT_DATA to send data

    /* Copy data message to the transmit message */
    for(int i = 0; i < length; i++) transmit_message.tx_data[i] = p_data[i];
    
    /* Send */
    can_message_transmit(CAN1, &transmit_message);
}

/* Receive CAN message interrupt */
void CAN1_RX1_IRQHandler(can_rx_buffer_t *pReceive_buffer){

    static can_receive_message_struct receive_message = {0};
    /* Here a shared buffer is used to store incoming messages for later processing */
    can_message_receive(CAN1, CAN_FIFO1, &receive_message);

    /* Put message in message buffer and handle in main loop */
    can_buffer_push(receive_message, &pReceive_buffer);
}
