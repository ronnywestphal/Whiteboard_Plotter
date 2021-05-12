#include "gd32vf103.h"
#include "delay.h"
#include <math.h>

#define CAN_RECEIVE_BUFFER_SIZE 32
#define CAN_NO_MESSAGE 0xFFF

#define CAN_GET_BUTTONS     0x600
#define CAN_GET_JOYSTICK    0x601
#define CAN_SET_LEDS        0x602
#define CAN_DRAW_LINE       0x603
#define CAN_EXECUTE         0x604
#define CAN_DRAW_CIRCLE     0x605
#define CAN_DRAW_MARIO      0x606
#define CAN_DRAW_SQUARE     0x607

// PWM 
#define PWMC1_PORT     GPIOA
#define PWMC1_PIN      GPIO_PIN_1
#define PWM_CHANNEL    





typedef struct{
    short int xcor;
    short int ycor;
}kordinat;


/* This is a fix for an earlier version of the API which did not include this interrupt. In later version CAN_INT_FLAG_RFL1 should be used */
#define CAN_RX_FIFO1_NOT_EMPTY (((uint32_t)(RFIFO1_REG_OFFSET) << 12) | ((uint32_t)(2U) << 6) | (uint32_t)(4U))


void travel(int x0, int y0, int x1, int y1);
kordinat plot_line (int x0, int y0, int x1, int y1,int x2,int y2);
kordinat drawcircle(int radie,int x0, int y0, int xst,int yst);
void mario();
void square(int lenght, int midX,int midY);

void CAN_receive_message_execute(can_receive_message_struct message,int P_coordinates[],short int *pX,short int *pY);
void CAN_send_message(uint16_t message_id, uint8_t remote_data, uint8_t length, uint8_t *p_data);
void init_ADC();
void init_PWM_example();
void pwm_up(void);
void pwm_down(void);


/* Some FIFO-functions for CAN messages */

const can_receive_message_struct can_no_message = {.rx_sfid = CAN_NO_MESSAGE, .rx_dlen = 0};

typedef struct{
    can_receive_message_struct receive_message_fifo[CAN_RECEIVE_BUFFER_SIZE];
    uint32_t tail;
    uint32_t head;
}can_rx_buffer_t;

can_rx_buffer_t receive_buffer;

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

void can_networking_init(void)
{
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




int main(void)
{
    //uint32_t debounce_counter = 0;
    //uint8_t buttons = 0;
    int P_coordinates[8];

    short int pointerX=0;             //PEKARE         startläget på plottern ugår från vad dessa värden är satta till.
    short int pointerY=0;             // PEKARE 

    //int32_t duty = 1000; // PWM DUTY

    can_receive_message_struct can_message;
    can_struct_para_init(CAN_RX_MESSAGE_STRUCT, &can_message);

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
    //gpio_init(GPIOB, GPIO_MODE_IN_FLOATING, GPIO_OSPEED_50MHZ, GPIO_PIN_2);

    //buttons = (gpio_input_port_get(GPIOB) >> 12) & 0x0F;

    init_PWM_example();   // Initiera PWM

    while(1){

        pwm_up();  // Grund vinkel PWM
        /* Start ADC conversion */
        adc_software_trigger_enable(ADC0, ADC_INSERTED_CHANNEL);

        /* Check receive buffer */
        can_message = can_buffer_pop(&receive_buffer);

        /* Check if there was a new message, if so execute corresponding functions */
        if(can_message.rx_sfid != CAN_NO_MESSAGE){
            CAN_receive_message_execute(can_message,P_coordinates, &pointerX,&pointerY);       
        } 

        //lyft penna  
    }
    
}

void CAN_receive_message_execute(can_receive_message_struct message,int P_coordinates[],short int *pX,short int *pY){
    
    kordinat tmp1;

    switch(message.rx_sfid)
    {

        case CAN_DRAW_LINE:
            if(message.rx_ft == CAN_FT_DATA){


                P_coordinates[0]=(message.rx_data[0] << 8)|(message.rx_data[1]);
                P_coordinates[1]=(message.rx_data[2] << 8)|(message.rx_data[3]);
                P_coordinates[2]=(message.rx_data[4] << 8)|(message.rx_data[5]);
                P_coordinates[3]=(message.rx_data[6] << 8)|(message.rx_data[7]);
                
                tmp1=plot_line (P_coordinates[0],P_coordinates[1],P_coordinates[2],P_coordinates[3],*pX,*pY);

                pwm_up(); //pen up
                *pX=tmp1.xcor;
                *pY=tmp1.ycor;

                // HÄR SKIFTAR VI         X0,Y0,X1,Y1   
            }
            break;



        case CAN_DRAW_CIRCLE:
             
                P_coordinates[0]=(message.rx_data[0] << 8)|(message.rx_data[1]);
                P_coordinates[1]=(message.rx_data[2] << 8)|(message.rx_data[3]);
                P_coordinates[2]=(message.rx_data[4] << 8)|(message.rx_data[5]);
                // P_coordinates[3]=(message.rx_data[6] << 8)|(message.rx_data[7]);



                tmp1=drawcircle(P_coordinates[0],P_coordinates[1],P_coordinates[2], *pX,*pY);
                pwm_up(); //pen up
                *pX=tmp1.xcor;
                *pY=tmp1.ycor;
                

                break;

        case CAN_DRAW_MARIO:
            if(message.rx_ft == CAN_FT_DATA){
                

                pwm_down();  // penn down
                mario();
                pwm_up(); //pen up
            }
            break;
        
        case CAN_DRAW_SQUARE:
            if(message.rx_ft == CAN_FT_DATA){
                
                pwm_down(); // penn down

                P_coordinates[0]=(message.rx_data[0] << 8)|(message.rx_data[1]);
                P_coordinates[1]=(message.rx_data[2] << 8)|(message.rx_data[3]);
                P_coordinates[2]=(message.rx_data[4] << 8)|(message.rx_data[5]);
                square(P_coordinates[0],P_coordinates[1],P_coordinates[2]);
                
                pwm_up(); //pen up
            
            }
            break;

        default:break;
    }
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
void CAN1_RX1_IRQHandler(void)
{
    static can_receive_message_struct receive_message = {0};
    /* Here a shared buffer is used to store incoming messages for later processing */
    can_message_receive(CAN1, CAN_FIFO1, &receive_message);

    /* Put message in message buffer and handle in main loop */
    can_buffer_push(receive_message, &receive_buffer);

}



/* Initialize two ADCs for joystick */
void init_ADC(){
    /* Initialize ADC pins */
    rcu_periph_clock_enable(RCU_GPIOA);
    gpio_init(GPIOA, GPIO_MODE_AIN, GPIO_OSPEED_50MHZ, GPIO_PIN_3 | GPIO_PIN_4);

    /* enable ADC clock */
    rcu_periph_clock_enable(RCU_ADC0);

    /* Select the clock frequency that will be used for the ADC core. */
    rcu_adc_clock_config(RCU_CKADC_CKAPB2_DIV4);    //DIV4 => 108/4 = 27MHz

    adc_deinit(ADC0);

    adc_mode_config(ADC_MODE_FREE);

    
    adc_special_function_config(ADC0, ADC_SCAN_MODE, ENABLE);
    

    /* Sets where padding is applied to the measurement. Data alignment right puts padding bits above MSB */
    adc_data_alignment_config(ADC0, ADC_DATAALIGN_RIGHT);

    /* Selects how many channels to convert each time. This can be used to "queue" multiple channels. Here just two channels are selected. */
    adc_channel_length_config(ADC0, ADC_INSERTED_CHANNEL, 2);

    /* Choose ADC0 channel 3 on the first "slot" and channel 4 to the second */
    adc_inserted_channel_config(ADC0, 0, ADC_CHANNEL_3, ADC_SAMPLETIME_55POINT5);
    adc_inserted_channel_config(ADC0, 1, ADC_CHANNEL_4, ADC_SAMPLETIME_55POINT5);

    /* Use software trigger, can't use continious conversion on the inserted channel */
    adc_external_trigger_source_config(ADC0, ADC_INSERTED_CHANNEL, ADC0_1_EXTTRIG_INSERTED_NONE);
    adc_external_trigger_config(ADC0, ADC_INSERTED_CHANNEL, ENABLE);
    
    /* Enable ADC.*/
    adc_enable(ADC0);

    /* Let ADC stabilize */
    delay_1ms(1);

    /* Calibrates the ADC against an internal source. */
    adc_calibration_enable(ADC0);

    adc_software_trigger_enable(ADC0, ADC_INSERTED_CHANNEL);
    
}

kordinat plot_line (int x0, int y0, int x1, int y1,int x2,int y2)
{   
    kordinat tmp;
    travel(x2,y2,x0,y0);
    
    pwm_down();//sätt penna
    
    ////////////////////////////////////////////
  int dx =   abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
  int dy = -abs(y1 - y0), sy = y0 < y1 ? 1 : -1; 
  int err = dx + dy, e2; /* error value e_xy */
  if(sx==1){
    gpio_bit_reset(GPIOA,GPIO_PIN_3);
  }else{
    gpio_bit_set(GPIOA,GPIO_PIN_3);
  }
  if(sy!=1){
    gpio_bit_reset(GPIOB,GPIO_PIN_0);
  }else{
    gpio_bit_set(GPIOB,GPIO_PIN_0);
  }
  
  
  for (;;){  /* loop */
    //setPixel (x0,y0);
    
    if (x0 == x1 && y0 == y1) break;
    e2 = 2 * err;
    
    if (e2 >= dy) { 
      err += dy; 
      x0 += sx; 
      gpio_bit_set(GPIOA,GPIO_PIN_4); 
     
      } /* e_xy+e_x > 0 */
    
    if (e2 <= dx) { 
      err += dx; 
      y0 += sy; 
      gpio_bit_set(GPIOB,GPIO_PIN_1); 
     
      } /* e_xy+e_y < 0 */

         
    delay_1us(800);
    gpio_bit_reset(GPIOA,GPIO_PIN_4);
    gpio_bit_reset(GPIOB,GPIO_PIN_1);
    delay_1us(800); 
  }
   
   tmp.xcor=x1;
   tmp.ycor=y1;
  return tmp;
}
kordinat drawcircle(int radie, int x0, int y0, int xst,int yst){

    kordinat tmp2;

    tmp2.xcor=x0;
    tmp2.ycor=y0;
    travel(xst,yst,x0+radie,y0);
    pwm_down();  // penn down

    
    
    int x_centre=x0;    //0
    int y_centre=y0;
    int x = radie, y = 0;
    int slutX=radie, slutY=0;
    int i=0;
    kordinat array[7000];

    array[i].xcor=(x + x_centre);
    array[i].ycor=(y + y_centre);
    i++;


    int P = 1 - radie;
    ////////////////////////////////////////////////////////////////////////////////////////////////////////
    while (x > y){ 
        y++;
          // Mid-point is inside or on the perimeter
        if (P <= 0)
            P = P + 2*y + 1;
              
        // Mid-point is outside the perimeter
        else
        {
            x--;
            P = P + 2*y - 2*x + 1;
        }  
        // All the perimeter points have already been printed
        if (x < y)
            break;

        array[i].xcor=x + x_centre;
        array[i].ycor=y + y_centre;
        i++;
        
        if (x != y)
        {
            array[i].xcor=y + x_centre;
            array[i].ycor=x + y_centre;
            i++;
           
        }
        
    } ////////////////////////////////////////////////////////////////////////////////////////////////////////
    /// sorterar efter X värden så vi vår 1/4 circel med streck.
    // slut kordinat
    array[i].xcor=slutY + x_centre;
    array[i].ycor=slutX + y_centre;
    i++; 
    ////////////////// SORTERAR ARRAYEN
    int rows=(i);
    kordinat tmp;
    
    for (int k = 0; k < rows ;k++){
        for (int j= 0; j < rows-1-k; j++){
            if (array[j].xcor<array[j+1].xcor){
                tmp=array[j];
                array[j]=array[j+1];
                array[j+1]=tmp;
            }    
        }   
    }  
    //// SKICKAR TILL motorerna
    for (int l = 0; l <(i-1); l++){
        travel(array[l].xcor,array[l].ycor,array[l+1].xcor,array[l+1].ycor);    // första kvadranten
                  // plus      plus    
    }

    // ___________________________________________   la till på kvällen (ta bort om de inte funkar) NEDANFÖR
    for (int p = i; p-1 > 0; p--){
        travel(-array[p-1].xcor,array[p-1].ycor,-array[p-2].xcor,array[p-2].ycor);    // andra kvadranten
    }                //minus        //plus


    for (int p = 0; p <(i-1); p++){
        travel(-array[p].xcor,-array[p].ycor,-array[p+1].xcor,-array[p+1].ycor);    // tredje kvadranten
                 // minus         //minus
    } 
    for (int p = i; p-1 > 0; p--){
        travel(array[p-1].xcor,-array[p-1].ycor,array[p-2].xcor,-array[p-2].ycor);

                //  plus           //minus
    }   

    return tmp2;

    
}
void mario(){

    
   
    



    // super mario!!!!!!!!!!
    //int x0=10,y0=10,x1=5,y1=3;
    int x1=0,x2=0,x3=500,x4=500,x5=1000,x6=1000,x7=0,x8=0,x9=500,x10=500,x11=1000,x12=1000,x13=1500,x14=1500,x15=1000,x16=1000,x17=500,x18=500,x19=1000,x20=1000,x21=1500,x22=1500,x23=4000,x24=4000,x25=5500,x26=5500,x27=4500,x28=4500,x29=5500,x30=5500,x31=6000,x32=6000,x33=5500,x34=5500,x35=4500,x36=4500,x37=5000,x38=5000,x39=5500,x40=5500,x41=6000,x42=6000,x43=5000,x44=5000,x45=5500,x46=5500,x47=6000,x48=6000,x49=4000,x50=4000,x51=3500,x52=3500,x53=2500,x54=2500,x55=2000,x56=2000,x57=0;
    int y1=0,y2=500,y3=500,y4=1000,y5=1000,y6=1500,y7=1500,y8=3500,y9=3500,y10=4000,y11=4000,y12=4500,y13=4500,y14=5000,y15=5000,y16=5500,y17=5500,y18=6500,y19=6500,y20=7500,y21=7500,y22=8000,y23=8000,y24=7500,y25=7500,y26=7000,y27=7000,y28=6500,y29=6500,y30=6000,y31=6000,y32=5500,y33=5500,y34=5000,y35=5000,y36=4500,y37=4500,y38=4000,y39=4000,y40=3500,y41=3500,y42=1500,y43=1500,y44=1000,y45=1000,y46=500,y47=500,y48=0,y49=0,y50=1000,y51=1000,y52=1500,y53=1500,y54=1000,y55=1000,y56=0,y57=0;
    //while(1){

        // SÄTT NER PENNA 
        travel(x1,y1,x2,y2);
        travel(x2,y2,x3,y3);
        travel(x3,y3,x4,y4);
        travel(x4,y4,x5,y5);
        travel(x5,y5,x6,y6);
        travel(x6,y6,x7,y7);
        travel(x7,y7,x8,y8);
        travel(x8,y8,x9,y9);
        travel(x9,y9,x10,y10);
        travel(x10,y10,x11,y11);
        travel(x11,y11,x12,y12);
        travel(x12,y12,x13,y13);
        travel(x13,y13,x14,y14);
        travel(x14,y14,x15,y15);
        travel(x15,y15,x16,y16);
        travel(x16,y16,x17,y17);
        travel(x17,y17,x18,y18);
        travel(x18,y18,x19,y19);
        travel(x19,y19,x20,y20);
        travel(x20,y20,x21,y21);
        travel(x21,y21,x22,y22);
        travel(x22,y22,x23,y23);
        travel(x23,y23,x24,y24);
        travel(x24,y24,x25,y25);
        travel(x25,y25,x26,y26);
        travel(x26,y26,x27,y27);
        travel(x27,y27,x28,y28);
        travel(x28,y28,x29,y29);
        travel(x29,y29,x30,y30);
        travel(x30,y30,x31,y31);
        travel(x31,y31,x32,y32);
        travel(x32,y32,x33,y33);
        travel(x33,y33,x34,y34);
        travel(x34,y34,x35,y35);
        travel(x35,y35,x36,y36);
        travel(x36,y36,x37,y37);
        travel(x38,y38,x39,y39);
        travel(x39,y39,x40,y40);
        travel(x40,y40,x41,y41);
        travel(x41,y41,x42,y42);
        travel(x42,y42,x43,y43);
        travel(x43,y43,x44,y44);
        travel(x44,y44,x45,y45);
        travel(x45,y45,x46,y46);
        travel(x46,y46,x47,y47);
        travel(x47,y47,x48,y48);
        travel(x48,y48,x49,y49);
        travel(x49,y49,x50,y50);
        travel(x50,y50,x51,y51);
        travel(x51,y51,x52,y52);
        travel(x52,y52,x53,y53);
        travel(x53,y53,x54,y54);
        travel(x54,y54,x55,y55);
        travel(x55,y55,x56,y56);
        travel(x56,y56,x57,y57);
}
void square(int length, int midX,int midY){

    kordinat start;
    start.xcor=(midX-(length/2));
    start.ycor=(midY-(length/2));

    kordinat slut;
    slut.xcor=(start.xcor+length);
    slut.ycor=(start.ycor+length);

    travel(0,0,start.xcor,start.ycor);

    travel(start.xcor,start.ycor,start.xcor,slut.ycor);  //streck rakt upp

    travel(start.xcor,slut.ycor,slut.xcor,slut.ycor);  //streck åt höger

    travel(slut.xcor,slut.ycor,slut.xcor,start.ycor);  // streck rakt ner

    travel(slut.xcor,start.ycor,start.xcor,start.ycor);
}




void travel(int x0, int y0, int x1, int y1)
{
    
    
    ////////////////////////////////////////////
  int dx =   abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
  int dy = -abs(y1 - y0), sy = y0 < y1 ? 1 : -1; 
  int err = dx + dy, e2; /* error value e_xy */
  if(sx==1){
    gpio_bit_reset(GPIOA,GPIO_PIN_3);
  }else{
    gpio_bit_set(GPIOA,GPIO_PIN_3);
  }
  if(sy!=1){
    gpio_bit_reset(GPIOB,GPIO_PIN_0);
  }else{
    gpio_bit_set(GPIOB,GPIO_PIN_0);
  }
  
  
  for (;;){  /* loop */
    //setPixel (x0,y0);
    
    if (x0 == x1 && y0 == y1) break;
    e2 = 2 * err;
    
    if (e2 >= dy) { 
      err += dy; 
      x0 += sx; 
      gpio_bit_set(GPIOA,GPIO_PIN_4); 
     
      } /* e_xy+e_x > 0 */
    
    if (e2 <= dx) { 
      err += dx; 
      y0 += sy; 
      gpio_bit_set(GPIOB,GPIO_PIN_1); 
     
      } /* e_xy+e_y < 0 */

         
    delay_1us(800);
    gpio_bit_reset(GPIOA,GPIO_PIN_4);
    gpio_bit_reset(GPIOB,GPIO_PIN_1);
    delay_1us(800); 
  }
   
}
void init_PWM_example(){

    /* These structs are used for configuring the timer */
    timer_oc_parameter_struct timer_ocinitpara;
    timer_parameter_struct timer_initpara;

    /* First we need to enable the clock for the timer */
    rcu_periph_clock_enable(RCU_TIMER4);

    /* Reset the timer to a known state */
    timer_deinit(TIMER4);

    /* This function sets the struct up with default values */
    timer_struct_para_init(&timer_initpara);

    /* timer configuration */
    timer_initpara.prescaler         = 107;                   // Prescaler 1 gives counter clock of 108MHz/2 = 54MHz 
    timer_initpara.alignedmode       = TIMER_COUNTER_EDGE;  // count alignment edge = 0,1,2,3,0,1,2,3... center align = 0,1,2,3,2,1,0
    timer_initpara.counterdirection  = TIMER_COUNTER_UP;    // Counter direction
    timer_initpara.period            = 20000;                // Sets how far to count. 54MHz/4096 = 13,2KHz (max is 65535)
    timer_initpara.clockdivision     = TIMER_CKDIV_DIV1;    // This is used by deadtime, and digital filtering (not used here though)
    timer_initpara.repetitioncounter = 0;                   // Runs continiously
    timer_init(TIMER4, &timer_initpara);                    // Apply settings to timer


    /* This function initializes the channel setting struct */
    timer_channel_output_struct_para_init(&timer_ocinitpara);
    /* PWM configuration */
    timer_ocinitpara.outputstate  = TIMER_CCX_ENABLE;                   // Channel enable
    timer_ocinitpara.outputnstate = TIMER_CCXN_DISABLE;                 // Disable complementary channel
    timer_ocinitpara.ocpolarity   = TIMER_OC_POLARITY_HIGH;             // Active state is high
    timer_ocinitpara.ocnpolarity  = TIMER_OCN_POLARITY_HIGH;    
    timer_ocinitpara.ocidlestate  = TIMER_OC_IDLE_STATE_LOW;            // Idle state is low
    timer_ocinitpara.ocnidlestate = TIMER_OCN_IDLE_STATE_LOW;
    timer_channel_output_config(TIMER4,TIMER_CH_1,&timer_ocinitpara);   // Apply settings to channel

    timer_channel_output_pulse_value_config(TIMER4,TIMER_CH_1,0);                   // Set pulse width
    timer_channel_output_mode_config(TIMER4,TIMER_CH_1,TIMER_OC_MODE_PWM0);         // Set pwm-mode
    timer_channel_output_shadow_config(TIMER4,TIMER_CH_1,TIMER_OC_SHADOW_DISABLE);

    /* auto-reload preload enable */
    timer_auto_reload_shadow_enable(TIMER4);

    /* start the timer */
    timer_enable(TIMER4);
}
void pwm_up(void){

  
  timer_channel_output_pulse_value_config(TIMER4,TIMER_CH_1,(int)1500);
  delay_1ms(20);
}
void pwm_down(){
  int j=1500;
  
  for(int i=0;i<500;i++){
    timer_channel_output_pulse_value_config(TIMER4,TIMER_CH_1,(int)j);
    delay_1ms(20);
    j+=5;
  }
}

