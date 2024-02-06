// This is an auto generated file by filter_designer.py
// You can modify this manually or regenerate it by running filter_designer.py
// See the README for more information
#ifndef IIR_CONFIG_H_
#define IIR_CONFIG_H_
#include "../fixed_point.h"
#define IIR_BIQUAD_NUM_TERMS 3
#define IIR_NUM_COEFFS       7
#define IIR_FILTER_ORDER     3
#define IIR_START_FREQ       40.0
#define IIR_STOP_FREQ        120.0
extern filter_coeff_t _iir_sos_coeffs[IIR_BIQUAD_NUM_TERMS][6];
extern filter_coeff_t _iir_b_coeffs[IIR_NUM_COEFFS];
extern filter_coeff_t _iir_a_coeffs[IIR_NUM_COEFFS];
#endif // ifndef IIR_CONFIG_H_
