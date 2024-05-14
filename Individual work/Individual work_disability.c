#include <stdio.h>
#include <math.h>



#define required_record 34 //(года)  Полный страховой стаж
#define minimal_record 15 //(года)  Минимально допустимый страховой стаж
#define standart_Pens_Age_Male 63 //(года)  стандартный пенсионный возраст Мужчин
#define standart_Pens_Age_Female 61 //(года)  стандартный пенсионный возраст Женщин
#define national_Insurance_Contribution 17522 //(леи) взнос обязательного гос страхования
#define insured_Income_Valorisation_Ccoefficient 2.07 //коэффициент валоризации застрахованного дохода
#define minimum_pension 2778 //(леи)  минимальная пенсия

// Функция для расчета среднемесячного застрахованного дохода
float calcAverageIncome(float income) {
    return income * 0.29;
}

float valorisedIncome(float CONi, float Kvi) {
    return CONi * Kvi;

}

// Функция для расчета пенсии по возрасту
float calcPensionByAge(float Tt, float Vav, float Rn, float R, float min_rec, float min_pension, float Vn , float Knp) {
    if (R >= Rn && Tt <= min_rec){
        if ((min_pension * Tt/(2 * min_rec) * Knp) < min_pension){
            return min_pension;
        } else{
        return (min_pension * Tt/(2 * min_rec) * Knp) ;
        }
    }
    if (R > Rn){
        Tt = Tt - (R - Rn);
        return  (0.0135 * Tt * Vav) + (0.02 * (R - Rn) * Vav);

    }else {
        if (Tt >= Vn && (0.0135 * Tt * Vav)<min_pension){
            return min_pension;
        }
        return  0.0135 * Tt * Vav;
    }

}



// Функция для расчета пенсии по инвалидности
float calcPensionDisability(float Vav, float Tt, float Tmax, int group) {
    if (group == 1) {
        if (0.42 * Vav + (Tt / Tmax) * Vav * 0.1 < minimum_pension){
            return minimum_pension;
        }else {
        return 0.42 * Vav + (Tt / Tmax) * Vav * 0.1;
        }
    } else if (group == 2) {
        if (0.35 * Vav + (Tt / Tmax) * Vav * 0.1 < minimum_pension){
            return minimum_pension;
        }else {
            return 0.35 * Vav + (Tt / Tmax) * Vav * 0.1;
        }

    } else  {
        if (0.20 * Vav + (Tt / Tmax) * Vav * 0.1 < minimum_pension){
            return minimum_pension;
        }else {
            return 0.20 * Vav + (Tt / Tmax) * Vav * 0.1;
        }
    }

}

int main() {
    float Vn = required_record;
    float min_rec = minimal_record;
    float Kvi = insured_Income_Valorisation_Ccoefficient;
    float Ci = national_Insurance_Contribution;
    float min_Pension = minimum_pension;
    float Rn; // Стандортный пенсионный возвраст
    char gender; // Гендер (М|Ж)
    float income; // Зарплата
    float R; //фактический возраст при выходе на пенсию
    float Vav; // валоризированный ежемесячный застрахованный доход
    float Tt; //страховой стаж
    float Knp; //коэффициент профессионального уровня
    float pension;
    Ci = round(Ci / 12); //1460   216000 262800
    printf("Male or Female:(M/F)");
    scanf("%c",&gender);
    if (gender == 'M'){
        Rn = standart_Pens_Age_Male;
    } else
    {
        Rn = standart_Pens_Age_Female;
    }
    float Tmax;
    int group;
    printf("Choose your disability group: \n");
    printf("3 - Medium disability group: \n");
    printf("2 - Accented disability group: \n");
    printf("1 - Severe disability group: \n");
    scanf("%d",&group);


    printf("Age at the date of disability determination: ");
    scanf("%f",&R);
    if (R < 23){
        Tmax = 2;
    } else if (23 <= R && R < 29){
        Tmax = 4;
    } else if (29 <= R && R < 33){
        Tmax = 7;
    } else if (33 <= R && R < 37){
        Tmax = 10;
    } else if (37 <= R && R < 41){
        Tmax = 13;
    }else {
        Tmax = 15;
    }

    printf("Insurance record: "); //страховой стаж
    scanf("%f",&Tt);

    printf("Enter your fixed income per month: ");// зарплата
    scanf("%f",&income);
    float CONi = calcAverageIncome(income);
    Vav = valorisedIncome(CONi, Kvi);
    printf("%f",Vav);

    // Расчет пенсии по инвалидности
    float pension_disability = calcPensionDisability(Vav, Tt, Tmax, group);
    printf("\nAmount of disability pension: %.2f\n", pension_disability);

//    return 0;
}
