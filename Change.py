import os

def convert(input_lst,output_type):
    type = input_lst[0][-3:]
    if not os.path.exists("output"):
        os.makedirs("output")
    
    match type:
        case "txt":
            
            match output_type:
                case "pdf":
                    from reportlab.pdfgen import canvas
                    
                    output_batch = []
                    file_names = []

                    for file_directory in input_lst:
                        with open(file_directory, 'r', encoding='utf-8') as txt_file:
                            content = txt_file.read()
                            

                        pdf_buffer  = canvas.Canvas(f"output/{os.path.basename(file_directory)}.pdf")

                        # Set font and size
                        pdf_buffer .setFont("Helvetica", 12)

                        # Split the content into lines
                        lines = content.split('\n')

                        # Set the starting y-coordinate for drawing text
                        y_coordinate = 700

                        # Draw each line of text
                        for line in lines:
                            pdf_buffer.drawString(30, y_coordinate, line)
                            y_coordinate -= 12  # Adjust this value based on your font size and line spacing
                        
                        pdf_buffer.save()

                    return 
     
                case "docx":
                    pass
            pass
        
        case "docx":
            match output_type:
                case "pdf":
                    pass
                case "txt":
                    pass
            
            pass
        
        case "pdf":
            match output_type:
                case "txt":
                    pass
                case "docx":
                    pass
            
            pass
        
        case "doc":
            match output_type:
                case "pdf":
                    pass
                case "txt":
                    pass
            
            pass
    