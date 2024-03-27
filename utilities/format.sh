#!/bin/bash
uncrustify -c utilities/format.cfg --no-backup impl/sma_filter/*.c
uncrustify -c utilities/format.cfg --no-backup impl/sma_filter/*.h
uncrustify -c utilities/format.cfg --no-backup example_impl/*.c
uncrustify -c utilities/format.cfg --no-backup impl/iir_filter/*.c
uncrustify -c utilities/format.cfg --no-backup impl/iir_filter/*.h
uncrustify -c utilities/format.cfg --no-backup impl/fir_filter/*.c
uncrustify -c utilities/format.cfg --no-backup impl/fir_filter/*.h
uncrustify -c utilities/format.cfg --no-backup impl/*.h