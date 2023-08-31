
.PHONY: main.ts synth deploy

convert: main.ts

main.ts:
	cat main.tf | cdktf convert > main.ts

synth:
	cdktf synth

deploy: synth
	cdktf deploy --skip-synth --auto-approve sedaro
