#include "Psync.h"

double pi = 3.141592653589793;
double e = 4.80320451e-10;
double c = 29979245800.0;
double m_e = 9.10938356e-28;
double h = 6.626e-27;


double Psync(double nu, double gamma, double B){
        double x = nu / ((3 * B * e) / (4 * pi * m_e * c) * gamma * gamma);
        return(
                1.808 * pow(x, 1 / 3) / pow(1 + 3.4*pow(x,2/3),1/2)
                * (1 + 2.21 * pow(x,2 / 3) + 0.347 * pow(x,4 / 3))
                / (1 + 1.353 * pow(x,2 / 3) + 0.217 * pow(x,4 / 3))
                * exp(-x)
              );
}
