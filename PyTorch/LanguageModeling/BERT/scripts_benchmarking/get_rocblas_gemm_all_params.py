import csv
from collections import Counter
op_list=[]

with open("results/bert_lamb_pretraining.pyt_bert_pretraining_phase2_fp16_gbs8.200803172442.log",'r') as f:
#with open("./test.log",'r') as f:
    for line in f:
        sub_list=[]
        if './rocblas-bench' in line:
            #sub_list=['gemm_type','transA','transB','m','n','k','alpha','lda','stride_a','ldb','stride_b','beta','ldc','stride_c','batch_count']
            string = line.split()
            #if cnt == 1:
            #    print(string)
            try:
                idx = string.index('./rocblas-bench')
            except ValueError:
                print("./rocblas-bench not present in list as is")
                for item in string:
                    if  './rocblas-bench' in item:
                        idx = string.index(item)
            for i in range(idx,len(string)):
                print("----------------------")
                print("string",string)
                print("i",i)
                stride_a_val = ''
                stride_b_val = ''
                stride_c_val = ''
                stride_d_val = ''
                batch_count_val = ''
                if string[i].find('gemm') != -1:
                    #params_dict.update([('gemm_type',param)])
                    sub_list.append(string[i])
                elif string[i] == '--transposeA':
                    #params_dict.update([('transA',param[i+1])])
                    sub_list.append(string[i+1])
                elif string[i] == '--transposeB':
                    #params_dict.update([('transB',param[i+1])])
                    sub_list.append(string[i+1])
                elif string[i] == '-m':
                    #params_dict.update([('m',param[i+1])])
                    sub_list.append(string[i+1])
                elif string[i] == '-n':
                    #params_dict.update([('n',param[i+1])])
                    sub_list.append(string[i+1])
                elif string[i] == '-k':
                    #params_dict.update([('k',param[i+1])])
                    sub_list.append(string[i+1])
                elif string[i] == '--alpha':
                    #params_dict.update([('alpha',param[i+1])])
                    sub_list.append(string[i+1])
                elif string[i] == '--lda':
                    #params_dict.update([('lda',param[i+1])])
                    sub_list.append(string[i+1])
                    sub_list.append(stride_a_val) ##Adding space for stride_a anyways, if it actuallly exists gets overwritten by next elif statement where last element of sub_list is overwritten. Similar startegy for stride_b, stride_c, batch_count
                elif string[i] == '--stride_a':
                    stride_a_val = string[i+1]
                #params_dict.update([('stride_a', stride_a)])
                    sub_list[-1] = stride_a_val
                elif string[i] == '--ldb':
                    #params_dict.update([('ldb',param[i+1])])
                    print("sub_list",sub_list)
                    sub_list.append(string[i+1])
                    sub_list.append(stride_b_val)
                elif string[i] == '--stride_b':
                    stride_b_val = string[i+1]
                #params_dict.update([('stride_b',stride_b)])
                    sub_list[-1] = stride_b_val
                elif string[i] == '--beta':
                    #params_dict.update([('beta',param[i+1])])
                    sub_list.append(string[i+1])
                elif string[i] == '--ldc':
                    #params_dict.update([('ldc',param[i+1])])
                    sub_list.append(string[i+1])
                    sub_list.append(stride_c_val)
                    #sub_list.append(batch_count_val)
                elif string[i] == '--stride_c':
                    stride_c_val = string[i+1]
                #params_dict.update([('stride_c',stride_c)])
                    sub_list[-1] = stride_c_val
                elif string[i] == '--ldd':
                    sub_list.append(string[i+1])
                    sub_list.append(stride_d_val)
                    sub_list.append(batch_count_val)
                elif string[i] == '--stride_d':
                    stride_d_val = string[i+1]
                    sub_list[-2] = stride_d_val
                elif string[i] == '--batch_count':
                    batch_count_val = string[i+1]
                #params_dict.update([('batch_count',batch_count)]))
                    sub_list[-1]=batch_count_val
                                   
            op_list.append(sub_list) 


                          
#print(op_list)
print(len(op_list))

list_of_tuples = [tuple(elem) for elem in op_list]
dct = dict(Counter(list_of_tuples))
lst = [list(e) for e in dct]
for elem in lst:
    elem.append(dct[tuple(elem)])

print(lst)
#with open('gemm_all_st2_amd_ph1_sgpu_bert_3_18.csv', mode='w') as csv_file:
#    csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL,
#                                    lineterminator='\n')
#
#    csv_writer.writerow(['gemm type', 'transA', 'transB', 'm', 'n', 'k']) 
#    for items in op_list:
#            csv_writer.writerow(items)         

with open('gemmallparams_1steps_ph2_bert_f16_bs8_withstride_d.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL,
                                    lineterminator='\n')
    #csv_writer.writerow(['gemm type', 'transA', 'transB', 'm', 'n', 'k', '#occurances'])
    csv_writer.writerow(['gemm_type','transA','transB','m','n','k','alpha','lda','stride_a','ldb','stride_b','beta','ldc','stride_c','batch_count','occurances'])
    for items in lst:
            csv_writer.writerow(items)         
