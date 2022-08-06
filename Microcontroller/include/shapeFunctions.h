#include "gd32vf103.h"


typedef struct{
    short int xcor;
    short int ycor;
}kordinat;

kordinat plot_line (int x0, int y0, int x1, int y1,int x2,int y2);
kordinat drawcircle(int radie,int x0, int y0, int xst,int yst);

void CAN_receive_message_execute(can_receive_message_struct message,int P_coordinates[],short int *pX,short int *pY);

void travel(int x0, int y0, int x1, int y1);
void mario();
void square(int lenght, int midX,int midY);
void pwm_up(void);
void pwm_down(void);
