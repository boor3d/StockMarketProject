#include <iostream>
#include <cmath>

// https://www.quantstart.com/articles/European-vanilla-option-pricing-with-C-and-analytic-formulae/

// M_PI = pi

// Standard normal probability density function 
double norm_pdf(const double& x)
{
    return (1.0 / (pow(stdM_PI, 0.5)))*stdexp(-.5*x*x);
}


// Recursive Function
// Approximation to the cumulative distribution function for standard normal distribution 
double norm_cdf(const double& x)
{
    double k = 1.0 / (1.0 + .2316419*x);
    double k_sum = k*(0.319381530 + k*(-0.356563782 + k*(1.781477937 + k*(-1.821255978 + 1.330274429*k))));

    if (x >= 0.0)
    {
        return (1.0 - (1.0/(pow(2*M_PI, .5)))*exp(-.5*x*x) * k_sum);
    }
    else
    {
        return 1.0 - norm_cdf(-x);
    }
}


double d_j(const int)




int main()
{
    return 0;
}