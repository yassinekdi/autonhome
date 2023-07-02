#define CMS_4_OUT 32
#define CMS_5_OUT 34

void setupCMS() {
}

void loopCMS(float &humidity_CMS4,float &humidity_CMS5) {
    int value_CMS_4, value_CMS_5;
    value_CMS_4= analogRead(CMS_4_OUT);
    humidity_CMS4 = ((value_CMS_4 - 3490) / (1584.7 - 3490)) * 100;
    humidity_CMS4 = constrain(humidity_CMS4, 0, 100);

    
    value_CMS_5= analogRead(CMS_5_OUT);
    humidity_CMS5 = ((value_CMS_5 - 3490) / (1584.7 - 3490)) * 100;
    humidity_CMS5 = constrain(humidity_CMS5, 0, 100);
}
