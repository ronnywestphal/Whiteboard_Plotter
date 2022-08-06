#include "gd32vf103.h"

#define CAN_RECEIVE_BUFFER_SIZE 32

typedef struct{
    short int xcor;
    short int ycor;
}kordinat;

typedef struct{
    can_receive_message_struct receive_message_fifo[CAN_RECEIVE_BUFFER_SIZE];
    uint32_t tail;
    uint32_t head;
}can_rx_buffer_t;

int can_buffer_push(can_receive_message_struct dat, can_rx_buffer_t *buf);

can_receive_message_struct can_buffer_pop(can_rx_buffer_t *buf);

void can_buffer_init(can_rx_buffer_t *buf);
void can_networking_init(void);

void CAN_send_message(uint16_t message_id, uint8_t remote_data, uint8_t length, uint8_t *p_data);
