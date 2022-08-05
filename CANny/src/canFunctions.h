#include "gd32vf103.h"


/* Some FIFO-functions for CAN messages */

typedef struct{
    can_receive_message_struct receive_message_fifo[CAN_RECEIVE_BUFFER_SIZE];
    uint32_t tail;
    uint32_t head;
}can_rx_buffer_t;

can_rx_buffer_t receive_buffer;

int can_buffer_push(can_receive_message_struct dat, can_rx_buffer_t *buf);

can_receive_message_struct can_buffer_pop(can_rx_buffer_t *buf);

void can_buffer_init(can_rx_buffer_t *buf);

/* END Compact FIFO for CAN messages */

/* This function contains all the code needed to configure the CAN-bus.
   It's a bit of a handfull but once it works right using it is fairly simple. */

void can_networking_init(void);

void CAN_receive_message_execute(can_receive_message_struct message,int P_coordinates[],short int *pX,short int *pY);
void CAN_send_message(uint16_t message_id, uint8_t remote_data, uint8_t length, uint8_t *p_data);