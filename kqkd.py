import pandas as pd

def kqkd(result_dthu, result_tkho, result_cphi):
    kqkd_th = result_dthu.iloc[3, 2] + result_tkho.iloc[0, 2] + result_cphi.iloc[0, 2]
    kqkd_ck = result_dthu.iloc[3, 3] + result_tkho.iloc[0, 3] + result_cphi.iloc[0, 3]
    kqkd_lk = result_dthu.iloc[3, 6] + result_tkho.iloc[0, 6] + result_cphi.iloc[0, 6]
    kqkd_ck_lk = result_dthu.iloc[3, 6] + result_tkho.iloc[0, 6] + result_cphi.iloc[0, 6]

    kqkd_ex_vm_th = result_dthu.iloc[3, 2] + result_tkho.iloc[0, 2] + result_cphi.iloc[0, 2] - result_dthu.iloc[5, 2] - result_tkho.iloc[2, 3]
    kqkd_ex_vm_ck = result_dthu.iloc[3, 3] + result_tkho.iloc[0, 3] + result_cphi.iloc[0, 3] - result_dthu.iloc[5, 3] - result_tkho.iloc[2, 3]
    kqkd_ex_vm_lk = result_dthu.iloc[3, 6] + result_tkho.iloc[0, 6] + result_cphi.iloc[0, 6] - result_dthu.iloc[5, 6] - result_tkho.iloc[2, 6]
    kqkd_ex_vm_ck_lk = result_dthu.iloc[3, 6] + result_tkho.iloc[0, 6] + result_cphi.iloc[0, 6] - result_dthu.iloc[5, 6] - result_tkho.iloc[2, 6]

    result_kqkd = pd.DataFrame(
        {
            'Chỉ Tiêu': ['LNTT', 'LNTT(-VM)', 'LNST', 'LNST(-VM)'],
            '': ['', '', '', ''],
            '  Thực Hiện  ': [kqkd_th, kqkd_ex_vm_th, kqkd_th * 0.8, kqkd_ex_vm_th * 0.8],
            '  Cùng Kỳ    ': [kqkd_ck, kqkd_ex_vm_ck, kqkd_ck * 0.8, kqkd_ex_vm_ck * 0.8],
            '  Kế Hoạch   ': [0 , 0, 0, 0],
            ' ': ['', '', '', ''],
            ' LK Thực Hiện': [kqkd_lk, kqkd_ex_vm_lk, kqkd_lk * 0.8, kqkd_ex_vm_lk * 0.8],
            ' LK Cùng Kỳ  ': [kqkd_ck_lk, kqkd_ex_vm_ck_lk, kqkd_ck_lk * 0.8, kqkd_ex_vm_ck_lk * 0.8],
            ' LK Kế Hoạch ': [0, 0, 0, 0],
            '  ': ['', '', '', ''],
            'LK Thực Hiện ': [kqkd_lk, kqkd_ex_vm_lk, kqkd_lk * 0.8, kqkd_ex_vm_lk * 0.8],
            '       KH Năm': [0 , 0, 0, 0]
        }
    )
    return result_kqkd