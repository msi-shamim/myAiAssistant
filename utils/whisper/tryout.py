def cli(**args):
    from whisper import available_models

    def valid_model_name(name):
        if name in available_models() or os.path.exists(name):
            return name
        raise ValueError(
            f"model should be one of {available_models()} or path to a model checkpoint"
        )

    args = parser.parse_args().__dict__

    # fmt: off
    args["audio"]=0
    args["model"]="small"
    args["model_dir"]=None
    args["device"]="cuda" if torch.cuda.is_available() else "cpu"
    args["output_dir"]="."
    args["output_format"]="all"
    args["verbose"]=True

    args["task"] ="transcribe"
    args["language"]="en"

    args["temperature"]=0
    args["best_of"]=5
    args["beam_size"]=5
    args["patience"]=None
    args["length_penalty"]=None

    args["suppress_tokens"]="-1"
    args["initial_prompt"]=None
    args["condition_on_previous_text"]=True
    args["fp16"]=True

    args["temperature_increment_on_fallback"]=0.2
    args["compression_ratio_threshold"]=2.4
    args["logprob_threshold"]=-1.0
    args["no_speech_threshold"]=0.6
    args["word_timestamps",]=False
    args["prepend_punctuations"]="\"\'“¿([{-"
    args["append_punctuations"]="\"\'.。,，!！?？:：”)]}、"
    args["highlight_words"]=False
    args["max_line_width"]=None
    args["max_line_count"]=None
    args["max_words_per_line"]=None
    args["threads"]=0
    # fmt: on

    model_name: str = args.pop("model")
    model_dir: str = args.pop("model_dir")
    output_dir: str = args.pop("output_dir")
    output_format: str = args.pop("output_format")
    device: str = args.pop("device")
    os.makedirs(output_dir, exist_ok=True)

    args["language"] = "en"

    temperature = args.pop("temperature")

    if (threads := args.pop("threads")) > 0:
        torch.set_num_threads(threads)

    from whisper import load_model

    model = load_model(model_name, device=device, download_root=model_dir)

    writer = get_writer(output_format, output_dir)
    word_options = [
        "highlight_words",
        "max_line_count",
        "max_line_width",
        "max_words_per_line",
    ]
    if not args["word_timestamps"]:
        for option in word_options:
            if args[option]:
                print(f"--{option} requires --word_timestamps True")
    if args["max_line_count"] and not args["max_line_width"]:
        print("--max_line_count has no effect without --max_line_width")
    if args["max_words_per_line"] and args["max_line_width"]:
        print("--max_words_per_line has no effect with --max_line_width")
    writer_args = {arg: args.pop(arg) for arg in word_options}
    for audio_path in args.pop("audio"):
        try:
            result = transcribe(model, audio_path, temperature=temperature, **args)
            writer(result, audio_path, **writer_args)
        except Exception as e:
            print(f"Skipping {audio_path} due to {type(e).__name__}: {str(e)}")