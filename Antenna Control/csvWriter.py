import csv

elem = [32.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
         None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
         None, None, None, None, None
        ]
import csv
 
def writeCsvLearning(input_file='csv/testTraining.csv', output_file='csv/testTraining.csv', new_column_data=elem, condition="no"):
    # Read the existing data from the CSV file
    data = []
    sizerow=len(new_column_data)
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        data = list(reader)
 
    if condition=="append":
        new_column_data=list(zip(new_column_data))
        # print(new_column_data)
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_column_data)

    else:
        new_column_data = list(reversed(list(new_column_data)))
    # Update the second column with new data
        for i, row in enumerate(reversed(list(data))):
            if i < len(new_column_data):
                    row.append(new_column_data[i])
                    # Update second column with new value
 
    # Write the modified data back to the CSV file
        with open(output_file, 'w+', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(data)
 

