#define CMS_4_OUT 32
// #define CMS_5_OUT 34
#define CMS_1_OUT 34

void setupCMS() {
}

void loopCMS(float &humidity_CMS4,float &humidity_CMS1) {
    int value_CMS_4, value_CMS_1;
    value_CMS_4= analogRead(CMS_4_OUT);
    humidity_CMS4 = ((value_CMS_4 - 4095) / (2196.28 - 4095)) * 100;
    humidity_CMS4 = constrain(humidity_CMS4, 0, 100);
    
    // value_CMS_5= analogRead(CMS_5_OUT);
    // humidity_CMS5 = ((value_CMS_5 - 4095) / (2138.1 - 4095)) * 100;
    // humidity_CMS5 = constrain(humidity_CMS5, 0, 100);

    value_CMS_1= analogRead(CMS_1_OUT);
    humidity_CMS1 = ((value_CMS_1 - 3490.1) / (1590 - 3490.1)) * 100;
    humidity_CMS1 = constrain(humidity_CMS1, 0, 100);
}
