/*

    WARNING: Não consegui fazer funcionar e rapidamente migrei para o micropython,
    não deve ser díficil de arrumar, mas real não precisa pq no main.py já se testa.

*/


#define R_TOP 34
#define R_MID 35
#define R_BOT 32

#define Y_TOP 33
#define Y_MID 25
#define Y_BOT 26

#define G_TOP 23
#define G_MID 22
#define G_BOT 21

#define ROWS_QTD 9

int row[] = [R_TOP, R_MID, R_BOT, Y_TOP, Y_MID, Y_BOT, G_TOP, G_MID, G_BOT];


void setup() {
    for (int i = 0; i < ROWS_QTD; i++)
        setPinMode(row[ROWS_QTD], OUTPUT);
}

bool intro = true;

void loop() {
    if (intro) {
        for (int i = 0; i < ROWS_QTD; i++)
        {
            digitalWrite(row[i], HIGH);
            delay(10);
        }
        delay(100);
        for (int i = 0; i < ROWS_QTD; i++)
        {
            digitalWrite(row[i], LOW);
            delay(10);
        }
        delay(100);
        for (int i = 0; i < ROWS_QTD; i++)
        {
            digitalWrite(row[i], HIGH);
            delay(10);
        }
        intro = false;
    }
}
