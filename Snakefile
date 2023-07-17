rule extract_adjs:
    input:
        "src/extract_adjs.py",
    output:
        "data/{language}/adjective_phrases.txt"
    shell:
        """
        mkdir -p data/{wildcards.language}
        cd src 
        python extract_adjs.py --lang {wildcards.language} --output_file ../data/{wildcards.language}/adjective_phrases.txt --num_sents 100000
        """

rule extract_adjs_all:
    input:
        expand("data/{language}/adjective_phrases.txt", language=["en", "fr", "ru", "ja", "it", "es"])