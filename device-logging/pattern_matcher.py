doc_list = ["aaa bbb ccc aaa".split(),
            "bbb aaa a12 ccc bbb".split(),
            "bbb ccc aaa aaa".split()
            ]

last_seen_index_aaa = None  # init'ed with no value

for doc_num, doc in enumerate(doc_list, start=1):
    for pos, char in enumerate(doc):
        if char == "aaa":
            last_seen_index_aaa = pos
        if char == "bbb":
            if last_seen_index_aaa is not None and pos > last_seen_index_aaa:
                print ("Found match in document %r " % doc_num)
                break  # no further match necessary





