class khu():
    is_life = False
    all_jy_count = 22
    all_jy_num = 2774.53
    day_avg = 4021.05
    jy_count = 11
    jy_num = 164.78
    jnlx_num = 0
    is_show = False
    is_ontime=False



aa = khu()
bb = aa.is_show * 100
print('bb',bb)
# print(ab.is_life)

zkjf={'10.00-9.80':100,'9.80-9.00':120,'9.00-8.50':130,'8.80-8.00':130,'8.00-7.00':150,'7.00-6.00':200,'6.00-0.00':300,}
lifezk = '10.00-9.80'
nowjf = 0
print('aa1212',aa,aa.is_life)
good = True
if aa.is_life:
    for key in zkjf:
        print(key + ':' + str(zkjf[key]))
        bb = key.split('-')
        print(float(bb[1]), float(aa.is_life), float(bb[0]),
              (float(aa.is_life) > float(bb[1]) and float(aa.is_life) <= float(bb[0])))
        if float(aa.is_life) > float(bb[1]) and float(aa.is_life) <= float(bb[0]):
            lifezk = key
            break
    print(aa.is_life, 'aaa', lifezk)

    # 本月积分  是否生活圈*100+Limit(交易总笔数*1,200)+Limit(int(总交易金额/100)*1,300)+Limit(int(日均/1000)*1,200)+Limit(交易笔数*1,10)+Limit(int(交易金额/100)*1,10)
    print('zkjf[lifezk]', zkjf[lifezk])
    nowjf = zkjf[lifezk] + (aa.all_jy_count * 1 if (aa.all_jy_count * 1 < 200) else 200) + (
        int(aa.all_jy_num / 100) if (int(aa.all_jy_num / 100) < 200) else 200) \
            + (int(aa.day_avg / 1000) if (int(aa.day_avg / 1000) < 200) else 200) \
            + (int(aa.jy_count / 1) if (int(aa.jy_count / 1) < 10) else 10) \
            + (int(aa.jy_num / 100) if (int(aa.jy_num / 100) < 10) else 10) \
            + (int(aa.jnlx_num / 500) if (int(aa.jnlx_num / 500) < 200) else 200) \
            + aa.is_show * 100 + good * 30 + aa.is_ontime * 50
    print(aa.icc_id, 'nowjf', nowjf)
else:
    nowjf = (aa.all_jy_count * 1 if (aa.all_jy_count * 1 < 200) else 200) + (
        int(aa.all_jy_num / 100) if (int(aa.all_jy_num / 100) < 200) else 200) \
            + (int(aa.day_avg / 1000) if (int(aa.day_avg / 1000) < 200) else 200) \
            + (int(aa.jy_count / 1) if (int(aa.jy_count / 1) < 10) else 10) \
            + (int(aa.jy_num / 100) if (int(aa.jy_num / 100) < 10) else 10) \
            + (int(aa.jnlx_num / 500) if (int(aa.jnlx_num / 500) < 200) else 200) \
            + int(aa.is_show * 100) + int(good * 30) + int(aa.is_ontime * 50)
    # print(aa.icc_id, 'nowjf', nowjf)



alljf = nowjf
print('alljf',alljf)
class khu1():
    is_life = False
    all_acc = 63
    all_jy_num = 2774.53
    day_avg = 4021.05
    jy_count = 11
    jy_num = 164.78
    jnlx_num = 0
    is_show = False
    is_ontime=False
bb = khu1()
if bb:
    alljf = bb.all_acc + nowjf - bb.is_show*100-zkjf[lifezk]
    if alljf<0:
        alljf=0
print('alljf',alljf)