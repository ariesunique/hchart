from flask_wtf import FlaskForm
from flask_wtf.file import  FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SubmitField

class InputForm(FlaskForm):
    ALLOWED_EXTENSIONS = ['csv']
    
    file = FileField('File', validators=[FileAllowed(ALLOWED_EXTENSIONS, 'csv files only!')])
    data = TextAreaField(description='Manually input data')
    submit = SubmitField("Submit")
    
    def validate(self):
        # first do the regular field-level validation
        if not FlaskForm.validate(self):
            return False
        
        # then verify that the user entered data manually or uploaded a file
        if not (self.data.data or self.file.data):
            self.data.errors.append("Please either manually input data OR upload a file.")
            return False

        return True
