#Importing libraries
import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd

dict1, dict2, col_values,std_attempt = {}, {}, [], {}
count1, count2, count3, count4, count5, count6, count7 = 0, 0, 0, 0, 0, 0, 0
  
#Reading the csv file
df_std = pd.read_csv('Wizzy.csv')
#df_std = pd.read_csv('newWizzy.csv')

#this strips trailing spaces in each column name cells
clean_col = [i.strip() for i in df_std.columns]
df_std.columns = clean_col

#creating a list of students
#student_list = [1]
student_list = list(set(val for val in df_std['Student No']))


def main():
    '''
    This is the main program that executes the creation of report card of all the students
    
    '''
    global dict1, dict2, col_values,std_attempt, count1, count2, count3, count4, count5, count6, count7
    
    for i in student_list:
        dict1, dict2, col_values,std_attempt, count1, count2, count3, count4, count5, count6, count7 = {}, {}, [], {}, 0, 0, 0, 0, 0, 0, 0
        creating_report(i)


def creating_report(student_num):
    '''This function takes in a
    Parameter
    ----------
    student_num : Integer
        DESCRIPTION.
    Student Identification Number

    Return: It returns an exported Report Card in a PDF format

    '''
    
    global count1, count2, count3, count4, count5, count6, count7
    
    df1 = df_std[df_std['Student No'] == student_num]
    
    #renaming long text column name
    df1.rename(columns = {'What you marked': 'Option marked', 'Outcome (Correct/Incorrect/Not Attempted)': 'Outcome', 'Time Spent on question (sec)': 'Time spent (Sec)'}, inplace = True)
    
    relevant_columns = ['Student No', 'Name of Candidate', 'Registration', 'Grade', 'Gender', 'Name of school', 'Date of Birth', 'City of Residence', 'Date and time of test', 'Country of Residence', 'Extra time assistance', 'Question No.', 'Time spent (Sec)', 'Score if correct', 'Score if incorrect', 'Attempt status', 'Option marked', 'Correct Answer', 'Outcome', 'Your score']
    
    #creating a data frame for each student based on the provided student number and selected relevant columns
    df_per_std = df1[relevant_columns]
    
    #create a new data frame 
    std = df_per_std
    
    #dropping irrelevant columns from students dataframe
    std = std.drop(['Student No', 'Name of Candidate', 'Registration', 'Grade', 'Gender',
       'Name of school', 'Date of Birth', 'City of Residence',
       'Date and time of test', 'Country of Residence',
       'Extra time assistance'], axis = 1)
    
    #creating a list of students dataframe column
    column_list = std.columns
    
    for i in std['Outcome']:
        if i == 'Correct':
            dict1[i] = 1 + count1
            count1 += 1
        elif i == 'Incorrect':
            dict1[i] = 1 + count2
            count2 += 1
        else:
            dict1[i] = 1 + count3
            count3 += 1
    
    #this creates two list of the column values and how many times they appear against the other
    perf = [key for key, val in dict1.items()]
    mark2 = [val for key, val in dict1.items()]
    
    for z in std['Attempt status']:
        if z == 'Attempted':
            std_attempt[z] = 1 + count6
            count6 += 1
        elif z == 'Unattempted':
            std_attempt[z] = 1 + count7
            count7 += 1
            
    remarks = [key for key, val in std_attempt.items()]
    marks = [val for key, val in std_attempt.items()]
    
    for w in std['Outcome']:
        if w == 'Correct':
            dict2[w] = 1 + count4
            count4 += 1
        elif w == 'Incorrect':
            dict2[w] = 1 + count5
            count5 += 1
        else:
            pass
    
    #this creates two list of two column values out of the three expected and how many times they appear against the other
    perf2 = [key for key, val in dict2.items()]
    mark3 = [val for key, val in dict2.items()]
    
    #ploting a Bar chart of the time spent in sec 
    plt.bar(std['Question No.'], std['Time spent (Sec)'])
    plt.title('Time Spent in Seconds')
    plt.xlabel('Question Number')
    plt.ylabel('Time in Seconds')
    plt.legend('Seconds')
    plt.savefig('time_sec.png')
    plt.show()
    
    
    #ploting the time in sec taken in hours
    plt.figure(0)
    plt.pie(std['Time spent (Sec)'], autopct = '%1.1f%%')
    plt.title('Time spent as a function of total time')
    plt.legend(labels = std['Question No.'], loc = 'best')
    plt.savefig('time_hrs.png')
    
    plt.figure(1)
    #ploting the Attempts and Unattempts made
    plt.pie(marks, autopct = '%1.1f%%')
    plt.title('Attempts')
    plt.legend(remarks, loc = 'best')
    plt.savefig('Attempts.png')
    
    plt.figure(2)
    #plotting the overall performance of the student
    plt.pie(mark2, autopct = '%1.1f%%')
    plt.title('Overall performance against the test')
    plt.legend(perf)
    plt.savefig('performance.png')
    
    plt.figure(3)
    #plotting the students performance based on correct and incorrect answers
    plt.pie(mark3, autopct = '%1.1f%%')
    plt.title('Accuracy from attempted questions')
    plt.legend(perf2)
    plt.savefig('Accuracy.png')
    plt.show()
    
    for c in range(len(std.columns)):
        col_values.append([])
        for val in std[column_list[c]]:
            col_values[c].append(val)
    
    #this converts each column name to a list for zipping
    columns = [[column_list[i]] for i in range(len(std.columns))]
    
    #this zips the columns with their values into a list called table
    table_list = [list(x) + y for x, y in zip(columns, col_values)]
    table = list(zip(*table_list))
    
    #extracting the first index position
    for ind in df_std.index[df_std['Student No'] == student_num]:
        num = ind
        break
    
    
    #student Biodata
    std_name = df1.loc[num, 'Name of Candidate']
    std_sch = df1.loc[num, 'Name of school']
    
    std_grade = df1.loc[num, 'Grade']
    city_res = df1.loc[num, 'City of Residence']
    
    country_res = df1.loc[num, 'Country of Residence']
    std_reg = df1.loc[num, 'Registration']
    
    std_gender = df1.loc[num, 'Gender']
    std_date_of_birth = df1.loc[num, 'Date of Birth']
    
    std_test_date = df1.loc[num, 'Date and time of test']
    std_time = df1.loc[num, 'Extra time assistance']
    total = df_per_std['Your score'].sum()
    
    #Entering the values into the Pdf
    name = f'Name of Candidate:  {std_name}'
    grade = f'Grade:  {std_grade}'
    
    sch_name = f'School Name:  {std_sch}'
    city_residence = f'City of Residence:  {city_res}'
    
    country_residence = f'Country of Residence:  {country_res}'
    reg_no = f'Registration No:  {std_reg}'
    
    gender = f'Gender:  {std_gender}' 
    date_of_birth = f'Date of birth:  {std_date_of_birth}'
    
    test_date = f'Date of Test:  {std_test_date}' 
    extra_time = f'Extra Time assistance:  {std_time}'
    
    #the student's total score
    total_score = f'Total Score = {total}'
    comment_set1 = '1. Is showing interest and enthusiasm for things we do. 2. Is cooperative and happy. 3. Volunteers often in class 4. Works hard. 5. Is self confident 6. Is helpful to others 7. Needs to imporve work habits 8. Fails to complete assignments on time'

    # Create instance of FPDF class
    # Letter size paper, use inches as unit of measure
    pdf=FPDF(orientation = 'L', format='A4', unit = 'in')
    
    # Add new page. Without this you cannot create the document.\
    pdf.add_page()
    
    # Effective page width, or just epw
    epw = pdf.w - 2*pdf.l_margin
    
    # Set column width to 1/4 of effective page width to distribute content 
    # evenly across table and page
    #col_width = epw/4
    
    pdf.set_font('Arial', 'B', 16.0)
    pdf.set_text_color(0, 0, 150)
    pdf.cell(11, 0.0, 'GREAT MINDS INSTITUTE REPORT CARD', align = 'R')
    pdf.ln(0.20)
    
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(10, 0.0, 'PERFORMANCE REPORT', align = 'L')
    pdf.ln(0.50)
    
    #setting text format
    pdf.set_font('Times', '', 12.5)
    pdf.set_text_color(0, 0, 0)
    
    #exporting the students passport
    pdf.image(f'{student_num}.jpg', x = 9.0, y = 1)
    pdf.ln(0.20)
    pdf.cell(6, 0.0, name)
    pdf.cell(10, 0.0, grade)
    pdf.ln(0.30)
    
    pdf.cell(6, 0.0, sch_name)
    pdf.cell(10, 0.0, city_residence)
    pdf.ln(0.30)
    
    pdf.cell(6, 0.0, country_residence)
    pdf.cell(10, 0.0, reg_no)
    pdf.ln(0.30)
    
    pdf.cell(6, 0.0, gender)
    pdf.cell(10, 0.0, date_of_birth)
    pdf.ln(0.30)
    
    pdf.cell(6, 0.0, test_date)
    pdf.cell(10, 0.0, extra_time)
    pdf.ln(0.50)
    
    th = pdf.font_size
    
    for data in table:
        for item in data:
            pdf.cell(1.25, th, str(item), border = 1)
        
        pdf.ln(0.20)
    pdf.ln(0.30)
    
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(11, 0.0, total_score, align = 'R')
    pdf.ln(0.25)
    
    pdf.set_font('Times', '', 10)
    pdf.cell(8, th, 'PERFORMANCE ANALYSIS.', align = 'C')
    pdf.ln(0.20)
    
    pdf.image('time_sec.png', x= 1, w = 2 )
    pdf.image('time_hrs.png', x = 3, y = 5, w = 2)
    pdf.image('performance.png', x = 5, y = 5, w = 2 )
    pdf.image('Attempts.png', x = 7, y = 5, w = 2 )
    pdf.image('Accuracy.png', x = 9, y = 5, w = 2 )
    
    #comments for the student.
    pdf.cell(8, th, 'Report Card Comments.', align = 'C')
    pdf.ln(0.20)
    pdf.multi_cell(epw, 0.15, comment_set1)
    pdf.ln(0.20)
    
    pdf.cell(4, 0.13, 'We appreciate your Patronage.........')
    pdf.cell(7, 0.0, 'Motor: KNOWLEDGE FOR EXCELLENCE', align = 'R')
    
    #exporting the report card
    pdf.output(std_name + '_ReportCard.pdf', 'F')
    
    print("Done")

    
'''
MAIN FUNCTION INVOCATION
'''
main()