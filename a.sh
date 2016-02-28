mkdir new_outputs
for i in {1..500}
do
	python evaluator_code.py 1 > new_outputs/$i
done
