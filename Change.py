import os

def convert(input_lst,output_type):
    type = input_lst[0][-3:]
    
    match type:
        case "txt":
            
            match output_type:
                case "pdf":
                    from reportlab.pdfgen import canvas
                    
                    output_batch = []

                    for file_directory in input_lst:
                        with open(file_directory, 'r', encoding='utf-8') as txt_file:
                            content = txt_file.read()

                        pdf_buffer  = canvas.Canvas("temp.pdf")

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


                        # Save the PDF file
                        output_batch.append(pdf_buffer )
                        
                        output_folder = "output"

                        # Create the output folder if it doesn't exist
                        if not os.path.exists(output_folder):
                            os.makedirs(output_folder)

                        for i, (pdf_buffer, input_file) in enumerate(zip(output_batch, input_lst)):
                            # Get the input file name without extension
                            input_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]

                            # Create the output PDF file name
                            output_file = os.path.join(output_folder, f"{input_name_without_extension}.pdf")

                            # Save the content to the output PDF file
                            with open(output_file, 'wb') as pdf_file:
                                pdf_buffer.save()

                                # Get the content from the buffer and write it to the file
                                pdf_file.write(pdf_buffer.getpdfdata())

                            print(f"Conversion completed. PDF saved to {output_file}")


                            

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
    