
.PHONY: main.ts synth

convert: main.ts

main.ts:
	cat main.tf | cdktf convert > main.ts

synth:
	cdktf synth
