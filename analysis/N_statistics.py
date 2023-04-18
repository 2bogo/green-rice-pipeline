import pandas as pd
import argparse

def read_contig(file_path):
    dic_seq = {}
    bulk = open(file_path).read()
    contig_list = bulk.split('>')
    for each in contig_list:
        if each == "": continue
        header = each.split('\n')[0]
        seq = ''.join(each.split('\n')[1:]).upper().replace('N','')
        if len(seq) < 200: continue
        dic_seq[header] = seq
        
    return dic_seq


def calc_contig_n(file_path):
    dic_seq = read_contig(file_path)
    output_list = []
    dic_seq_keys = list(dic_seq.keys())
    dic_seq_keys.sort(key = lambda x: len(dic_seq[x]))
    total_length = sum([len(i) for i in dic_seq.values()])

    output_list.append(len(dic_seq_keys))
    output_list.append(total_length)
    output_list.append(len(dic_seq[dic_seq_keys[-1]]))
    output_list.append(len(dic_seq[dic_seq_keys[0]]))
    
    N_list = [int(total_length * i * 0.1)for i in range(1,10)][::-1]
    
    stack = 0
    
    n_output_list = []
    for c in dic_seq_keys:
        i = 10
        for n in N_list:
            if stack <= n < stack + len(dic_seq[c]):
                n_output_list.append(len(dic_seq[c]))
            i += 10
        stack += len(dic_seq[c])
    
    return output_list + n_output_list[::-1]










def main(args):
    data = [calc_contig_n(f) for f in args.file_list]

    # columns
    c = ['Number of contig', 'Total length', 'Max.', 'Min.'] + [f'N{str(i*10)}' for i in range(1, 10)]
    
    # filetering
    df = pd.DataFrame(data, columns=c, index=[i.split('/')[-1] for i in args.file_list])

    # save file
    df[['Number of contig', 'N50', 'Min.', 'Max.', 'Total length']].T.to_csv(f'{args.output_path}/N_statistics.csv')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="contig N_statistics")
    parser.add_argument('file_list', nargs='+', type=str, help="list of assembly files")
    parser.add_argument('-o', dest="output_path", type=str, help="output folder path")

    args = parser.parse_args()
    main(args)
    
    