#include "Psync.h"

const double pi = 3.141592653589793;
const double e = 4.80320451e-10;
const double c = 29979245800.0;
const double m_e = 9.10938356e-28;
const double h = 6.626e-27;


double Psync(const double nu, const double gamma, const double B){
        double x = nu / ((3.0*B*e) / (4.0*pi*m_e*c) * gamma*gamma);
        double powX_2over3 = pow(x, 2.0/3.0);
        double powX_4over3 = pow(x, 4.0/3.0);

        return(
                1.808*pow(x, 1.0/3.0) / pow(1.0 + 3.4*powX_2over3,1.0/2.0)
                * (1.0 + 2.21*powX_2over3 + 0.347*powX_4over3)
                / (1.0 + 1.353*powX_2over3 + 0.217*powX_4over3)
                * exp(-x)
              );
}
