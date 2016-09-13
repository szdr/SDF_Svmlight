# -*- coding: utf-8 -*-
import csv
import argparse
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
import numpy as np


def calc_fingerprint(mol, fingerprint="Morgan"):
    if fingerprint == "Morgan":
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    fp_str = DataStructs.cDataStructs.BitVectToText(fp)
    fp_lst = list(fp_str)
    fp_arr = np.array(fp_lst, dtype=int)
    return fp_arr


def format_svmlight(score, fp_arr, comment):
    # fp_arr -> fp_svmlight
    nonzero_index = np.nonzero(fp_arr)[0]
    desc_lst = [str(i + 1) + ":1" for i in nonzero_index]
    ret = [score] + desc_lst + ["#", comment]
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Convert PubChem sdf to svmlight")
    parser.add_argument("pubchem_sdf")
    parser.add_argument("datatable")
    parser.add_argument("score_name")
    parser.add_argument("-o", "--out_file", default="./out.svmlight")
    args = parser.parse_args()

    datatable_dict = {}
    with open(args.datatable) as datatable_fp:
        reader = csv.DictReader(datatable_fp)
        for row in reader:
            sid = row["PUBCHEM_SID"]
            score = row[args.score_name]
            if score == "":  # not reported
                continue
            activity = row["PUBCHEM_ACTIVITY_OUTCOME"]
            datatable_dict[sid] = (score, activity)

    input_mols = Chem.SDMolSupplier(args.pubchem_sdf)
    with open(args.out_file, "w") as out_fp:
        writer = csv.writer(out_fp, delimiter=" ")
        N = len(input_mols)
        for i, input_mol in enumerate(input_mols):
            print("{} in {}".format(i + 1, N))
            if input_mol is None:
                print("compound {} is None".format(i))
                continue
            sid = input_mol.GetProp("PUBCHEM_SUBSTANCE_ID")
            score, activity = datatable_dict[sid]
            fp_arr = calc_fingerprint(input_mol)
            comment = "{}:{}".format(sid, activity)
            row_svmlight = format_svmlight(score, fp_arr, comment)
            writer.writerow(row_svmlight)
