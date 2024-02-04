// This is an auto generated file by iir_design.py
// You can modify this manually or regenerate it by running iir_design.py
// See the README for more information
#ifndef IIR_CONFIG_H_
#define IIR_CONFIG_H_
#include "../fixed_point.h"
#define IIR_BIQUAD_NUM_TERMS 8
#define IIR_FILTER_ORDER 15
#define IIR_START_FREQ 0.5
#define IIR_STOP_FREQ 0
extern filter_coeff_t _iir_sos_coeffs[IIR_BIQUAD_NUM_TERMS][6];
extern filter_coeff_t _iir_b_coeffs[IIR_FILTER_ORDER + 1];
extern filter_coeff_t _iir_a_coeffs[IIR_FILTER_ORDER + 1];
#endif