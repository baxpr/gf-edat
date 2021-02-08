#!/bin/bash

# Initialize defaults (will be changed later if passed as options)
export project=NO_PROJ
export subject=NO_SUBJ
export session=NO_SESS
export src_dir=/opt/gf-edat/src

# Parse options
while [[ $# -gt 0 ]]
do
	key="$1"
	case $key in
		--project)
			export project="$2"; shift; shift ;;
		--subject)
			export subject="$2"; shift; shift ;;
		--session)
			export session="$2"; shift; shift ;;
		--scan)
			export scan="$2"; shift; shift ;;
		--task)
			export task="$2"; shift; shift ;;
		--eprime_txt)
			export eprime_txt="$2"; shift; shift ;;
		--out_dir)
			export out_dir="$2"; shift; shift ;;
		--src_dir)
			export src_dir="$2"; shift; shift ;;
		*)
			echo Unknown input "${1}"; shift ;;
	esac
done

# Convert E-Prime's .txt to a table format CSV file
eprime_csv="${out_dir}"/eprime.csv
${src_dir}/eprime_to_csv.py --outcsv "${eprime_csv}" "${eprime_txt}"

# Parse for the specific task (Oddball, WM, SPT)
summary_csv="${out_dir}"/eprime_summary_${task}.csv
"${src_dir}"/parse_csv_GF_${task}.py --outcsv "${summary_csv}" "${eprime_csv}"

# Create PDF
summary_pdf="${out_dir}"/eprime_summary.pdf
python -c 'from fpdf import FPDF; pdf = FPDF(); pdf.add_page(); pdf.set_font("Courier", size = 9);
f = open("'$TEXTFILE'", "r",encoding="latin-1");
for line in f:
	x = line.encode("latin1","ignore").decode("latin1")
	pdf.multi_cell(193, 5, txt = x);
pdf.output("'$PDFFILE'")'

# Organize files into dirs so we don't need to know the filenames for the yaml
mkdir "${out_dir}"/EPRIME_CSV
mv "${eprime_csv}" "${out_dir}"/EPRIME_CSV
mkdir "${out_dir}"/SUMMARY_CSV
mv "${summary_csv}" "${out_dir}"/SUMMARY_CSV

