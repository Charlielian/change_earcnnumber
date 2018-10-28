import csv
import configparser
import datetime,time





hell0_str = 'hello,this is start！ Good Lucy！！！'


config = configparser.ConfigParser()    # 注意大小写
config.read("config.ini")   # 配置文件的路径


def band_list():
    band_list = config.options('band')
    # print(band_list)
    f2b = {}
    for item in band_list:
        pp = config.get('band', item)
        pl = pp.split(',')
        for kk in pl:
            f2b[kk] = item
    return f2b

def feq_rule():
    rule_list = config.options('earfcn_num')
    f2r = {}
    for item in rule_list:
        rule = config.get('earfcn_num',item)
        rule_list = rule.split(',')
        #print(rule_list)
        f2r[item] = {}
        for num in range(len(rule_list)):
            feq = rule_list[num].strip()
            f2r[item][feq] = num+1


    #print(f2r)
    return f2r
def feqtband(feq,f2b):
    if feq in f2b.keys():
        band_item = f2b[feq]
    else:
        band_item =''
    return band_item


def readcsv(path,filename,header):
    if path is None: # path 为文件路径，如path 为None则读取同文件夹的文件
        f = open( filename,'r',encoding = 'utf-8')
    else:
        f = open(path +"\\" + filename,'r',encoding = 'utf-8')

    p_list =[]
    header_list = []
    num =0
    for line in f :
        num +=1
        if num == 1 : #判断是否第一行
            # print(line)
            line_list = line.split(',')
            # print(line_list)
            l_list = []
            for item in line_list:
                context = item.replace('"', '').replace('\n', '')
                l_list.append(context)
            header_list.append(l_list)
        else:
            # print(line)
            line_list = line.split(',')
            # print(line_list)
            l_list = []
            for item in line_list:
                context = item.replace('"', '').replace('\n', '')
                l_list.append(context)
            p_list.append(l_list)


    #print(p_list)

    f.close()
    return p_list,header_list


def layers(cellid):
    #print(cellid,type(cellid))

    if cellid in ['1', '2', '3', '129', '130', '131', '65', '66', '67']:
        layer = 1
    elif cellid in ['4', '5', '6', '132', '133', '134', '68', '69', '70']:
        layer = 2
    elif cellid in ['7', '8', '9', '135', '136', '137', '71', '72', '73']:
        layer = 3
    else:
        layer =0
    return layer


def sitetype(cel_dict):
    max_layer = 0
    for item in cel_dict.keys():
        #print(cel_dict[item][3],type(cel_dict[item][3]))
        if cel_dict[item][3]>max_layer:
            max_layer = cel_dict[item][3]

    tra2str = {3:'triple' ,1:'single' ,2:'double'}
    site_type = tra2str[max_layer]
    #print(site_type)
    return site_type



def lnho_type(lnhoif_list):
    enb_dict = {}
    for item in lnhoif_list:
        enbid = item[0]
        cellid = item[1]
        lnhoid = item[4]
        #print(lnhoid ,type(lnhoid))
        adj_earfcn = item[5]
        para_list = []
        for num in range(6, 27):
            para_list.append(item[num])
        #print(enbid,cellid,lnhoid,adj_earfcn)
        if enbid in enb_dict.keys():
            if cellid in enb_dict[enbid].keys():
                enb_dict[enbid][cellid][adj_earfcn] =[para_list, lnhoid]
            else:
                enb_dict[enbid][cellid] ={}
                #enb_dict[enbid][cellid][adj_earfcn] = []
                enb_dict[enbid][cellid][adj_earfcn] = [para_list, lnhoid]
        else:
            enb_dict[enbid] = {}
            enb_dict[enbid][cellid] = {}
            enb_dict[enbid][cellid][adj_earfcn]=[]
            #para_list = []
            #print(enb_dict[enbid][cellid][adj_earfcn])
            #print(enbid, cellid, adj_earfcn, para_list)
            #print("不存在")
            enb_dict[enbid][cellid][adj_earfcn] = [para_list, lnhoid]
            #enb_dict[enbid][cellid]['number'] = lnhoid

    return enb_dict
def cel_type(lncel_list,f2b,target_list):
    # 读取config文件的频段对应频点列表
    #进行enb字典汇总
    enb_dict ={}




    for item in lncel_list:
        enbid = item[2]
        cellid = item[3]
        ver = item[4]
        Aerfcn = item[5]
        layer = layers(cellid)
        band = feqtband(Aerfcn, f2b)
        if len(target_list) > 0:
            if enbid in target_list:
                if enbid in enb_dict.keys():
                    # enb_dict[item[2]] = {}
                    # 创建字典，存版本，小区频点，站点类型，频段，层数,类型
                    enb_dict[enbid][cellid] = [ver, Aerfcn, band, layer, '']
                    site_type = sitetype(enb_dict[enbid])
                    for cel_item in enb_dict[enbid]:
                        enb_dict[enbid][cel_item][4] = site_type
                        # print(cel_item)

                    # enb_dict[enbid][cellid] = [ver, Aerfcn, band, layer, site_type]
                    # pass
                else:
                    enb_dict[enbid] = {}
                    enb_dict[enbid][cellid] = [ver, Aerfcn, band, layer, 'single']
                    site_type = sitetype(enb_dict[enbid])
                    enb_dict[enbid][cellid] = [ver, Aerfcn, band, layer, site_type]

        else:
            if enbid in enb_dict.keys():
                # enb_dict[item[2]] = {}
                # 创建字典，存版本，小区频点，站点类型，频段，层数,类型
                enb_dict[enbid][cellid] = [ver, Aerfcn, band, layer, '']
                site_type = sitetype(enb_dict[enbid])
                for cel_item in enb_dict[enbid]:
                    enb_dict[enbid][cel_item][4] = site_type
                    # print(cel_item)

                # enb_dict[enbid][cellid] = [ver, Aerfcn, band, layer, site_type]
                # pass
            else:
                enb_dict[enbid] = {}
                enb_dict[enbid][cellid] = [ver, Aerfcn, band, layer, 'single']
                site_type = sitetype(enb_dict[enbid])
                enb_dict[enbid][cellid] = [ver, Aerfcn, band, layer, site_type]
    return enb_dict

def list2str(list):

    for item in list:
        pass

def main(cel_dict,rule,lnho_dict):
    del_list = []
    update_list = []
    add_list = []

    for enb in cel_dict.keys():
        # print("开始匹配",enb)
        for cel in cel_dict[enb].keys():
            print('正在匹配',enb+'_'+cel)
            # 拼接类型+频点
            celtype = cel_dict[enb][cel][4] + '_' + cel_dict[enb][cel][1]
            ver = cel_dict[enb][cel][0]
            # print(celtype)
            if celtype in rule.keys():  # 拼接类型+频点搜索在规则内
                # print(enb,rule[celtype])
                cur_list = rule[celtype]
                for feq_str in cur_list.keys():
                    #print(feq_str)
                    new_num = cur_list[feq_str]
                    if enb in lnho_dict.keys():
                        if cel in lnho_dict[enb].keys():
                            if feq_str in lnho_dict[enb][cel].keys():
                                old_num = lnho_dict[enb][cel][feq_str][1]
                                if old_num == new_num:
                                    pass
                                else:
                                    del_list.append([enb, cel, ver, old_num])
                                    n_list = [enb, cel, ver,new_num, feq_str]
                                    for item in lnho_dict[enb][cel][feq_str][0]:
                                        n_list.append(item)
                                    update_list.append(n_list)
                            else:
                                #print("当前异频配置没有该频点！！",enb , ',' , cel , ',' , ver ,',' ,key ,',' ,new_num)
                                #context = "当前异频配置没有该频点！！  " + enb + ',' + cel + ',' +key
                                add_list.append([enb  , cel ,  ver ,feq_str ,new_num,'漏定义频点' ])
                        else:
                            feq_dict = rule[celtype]
                            for ff in feq_dict.keys() :
                                #print("当前异频配置没有该cellid！！", enb, ',', cel, ',', ver,ff,feq_dict[ff])
                                #context = "当前异频配置没有该cellid！！  " + enb + ',' + cel
                                add_list.append([enb, cel, ver, ff, feq_dict[ff], '漏定义频点_没有cellid'])
                    else:
                        for cel in cel_dict[enb].keys():
                            celtype = cel_dict[enb][cel][4] + '_' + cel_dict[enb][cel][1]
                            if celtype in rule.keys():
                                feq_dict =rule[celtype]
                                for feq_item in feq_dict.keys():
                                    #print("当前异频配置没有该enbid！！", enb, ',', cel, ',', ver, feq_item, feq_dict[feq_item])
                                    add_list.append([enb, cel, ver, feq_item, feq_dict[feq_item], '漏定义频点_没有enbid'])
                            else:
                                #print(enb, cel, cel_dict[enb][cel][4] + '_' + cel_dict[enb][cel][1], "小区类型不在预设的列表里，请检查规则")
                                pass

                        print("当前异频配置没有该enbid！！",enb)
                        context = "当前异频配置没有该enbid！！  " + enb

                # for
            else:
                print(enb,cel,cel_dict[enb][cel][4]+ '_' +cel_dict[enb][cel][1],"小区类型不在预设的列表里，请检查规则")
                context = enb, cel, cel_dict[enb][cel][1], cel_dict[enb][cel][4]
                # 增加错误log，出错提示！！
    return del_list,update_list,add_list
def list2csv(filename,list_str):
    time_s =datetime.datetime.now()
    time_str = time_s.strftime( '%Y%m%d%H%M%S' )
    #filename = list_str.name().replace("_list",'')
    with open("%s_%s.csv"%('file' +"\\" +filename,time_str), "w", newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        for line in list_str:
        #for item in line:
            csvwriter.writerow(line)

    #f.close()

if __name__ == '__main__':
    print(hell0_str)
    starttime = datetime.datetime.now()
    f2b = band_list()

    cel_file = config.get('main', 'lncel_file')
    lnhoif_file = config.get('main', 'lnhoif_file')
    target = config.get('target', 'enbid')
    target_list = target.split(',')
    rule = feq_rule()
    #readcsv(None,'lnhoif_1025.csv')
    lncel_list ,lncel_header= readcsv(None, cel_file,0)
    #print(type(lncel_list))
    #for item in lncel_list
    cel_dict = cel_type(lncel_list,f2b,target_list)

    lnhoif ,lnhoif_header= readcsv(None, lnhoif_file,1)
    #print(lnhoif_header)
    lnho_dict = lnho_type(lnhoif)

    del_list,update_list ,add_list = main(cel_dict, rule, lnho_dict)
    #print(del_list)
    #print(update_list)
    #
    list2csv('deldata',del_list)
    list2csv('updatedata', update_list)
    list2csv('adddata', add_list)
    ########################
    endtime = datetime.datetime.now()
    print(endtime - starttime)

















