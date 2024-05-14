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
    printf("Enter your fixed income per month: ");// зарплата
    scanf("%f",&income);
    float CONi = calcAverageIncome(income);
    printf("Insurance record: "); //страховой стаж
    scanf("%f",&Tt);
    printf("\nAverage monthly insured income: %.2f\n", CONi); //сумма взносов социального страхования
    if (CONi < Ci){
        Tt = round((Tt * (CONi/Ci)) * 10.0) / 10.0;
    }
    printf("Proven insurance record: %.1f\n", Tt);//страховой стаж с условием малого страхового дохода
    Vav = valorisedIncome(CONi, Kvi);
    printf("Enter your retirement age: "); //фактический возраст при выходе на пенсию
    scanf("%f",&R);
    printf("Choose your occupational rate: \n");
    printf("1 - for agricultural workers, labourers (I-II qualification category) and unskilled auxiliary personnel: \n");
    printf("2 - for medium-skilled workers (III-IV qualification category): \n");
    printf("3 - for highly qualified workers (V-VIII qualification category) and specialists with specialised secondary education: \n");
    printf("4 - for professionals with higher education: \n");
    printf("5 - for executives at the level of structural subdivision: \n");
    printf("6 - for heads of enterprises and their deputies: \n");
    int choice;
    scanf("%d",&choice);

    switch (choice) {
        case 1:
            Knp = 1;
            break;
        case 2:
            Knp = 1.2;
            break;
        case 3:
            Knp = 1.5;
            break;
        case 4:
            Knp = 1.8;
            break;
        case 5:
            Knp = 2.0;
            break;
        case 6:
            Knp = 3.0;
            break;
        default:
            Knp = 1;
            break;
    }




    // Расчет пенсии по возрасту
    pension = calcPensionByAge(Tt, Vav, Rn, R, min_rec, min_Pension, Vn, Knp);
    printf("Amount of retirement pension: %.2f\n", pension); //Размер пенсии по возрасту
}
