#!/bin/bash

# Initialize defaults (will be changed later if passed as options)
export project=NO_PROJ
export subject=NO_SUBJ
export session=NO_SESS
export scan=NO_SCAN
export task=UNSPECIFIED
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

# Verify the specified task is in the list we can handle
case "${task}" in
	Oddball|OddballOld|SPT|SPT-ESOP|WM)
		;;
	*)
		echo Unknown task "${task}"
		exit 1
		;;
esac


# Convert E-Prime's .txt to a table format CSV file
echo Converting to CSV: "${eprime_txt}"
eprime_csv="${out_dir}"/eprime.csv
case "${task}" in
	Oddball|OddballOld|SPT|WM)
        ${src_dir}/eprime_to_csv.py --outcsv "${eprime_csv}" "${eprime_txt}"
		;;
	*)
        ${src_dir}/eprime_to_csv_unsorted.py --outcsv "${eprime_csv}" "${eprime_txt}"
		;;
esac


# Parse for the specific task (Oddball, WM, SPT)
echo Parsing: "${eprime_csv}"
summary_csv="${out_dir}"/eprime_summary_${task}.csv
"${src_dir}"/parse_csv_GF_${task}.py --outcsv "${summary_csv}" "${eprime_csv}"

# Create PDF
echo Creating PDF
summary_pdf="${out_dir}"/eprime_summary.pdf
"${src_dir}"/make_pdf.py  --incsv "${summary_csv}" --outpdf "${summary_pdf}" \
	--project "${project}" --subject "${subject}" --session "${session}" --scan "${scan}" \
	--task "${task}"

# Organize files into dirs so we don't need to know the filenames for the yaml
echo Organizing outputs
mkdir -p "${out_dir}"/EPRIME_CSV
mv "${eprime_csv}" "${out_dir}"/EPRIME_CSV
mkdir -p "${out_dir}"/SUMMARY_CSV
mv "${summary_csv}" "${out_dir}"/SUMMARY_CSV

