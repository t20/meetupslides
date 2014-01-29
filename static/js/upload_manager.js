MeetupSlides = {
    clearColors: function(obj){
       obj.removeClass("has-warning");
       obj.removeClass("has-error");
       obj.removeClass("has-success");                           
    },                            
                
    textValidator: function(selector, type, text) {
        var validation_result = true;                                           
        $(selector).each(function(k, v){       
            MeetupSlides.clearColors($(this));                                                        
            if ($(this).find(type).val() == text){
                $(this).addClass('has-error'); 
                validation_result = false;                                                  
            }else{
                $(this).addClass('has-success');        
            }                                                 
        });  
        return validation_result;                                                                                                    
    },               
    validateUpload : function(){
        speaker_validation = MeetupSlides.textValidator('.validate-speaker', 'input', 'Speaker Name');
        //meetup_name_validation = MeetupSlides.textValidator('.validate-meetup-name', 'input', 'Meetup Name');
        title_validation = MeetupSlides.textValidator('.validate-title', 'input', 'Presentation title');
        description_validation = MeetupSlides.textValidator('.validate-description', 'textarea', 'A brief description of the talk.');
                
        if (speaker_validation == true  && title_validation == true && description_validation == true){
           return true;    
        }else{
           return false;
        }                                                                                                 
    },
    
    
    generateFormDataParams : function(){
     // Add all the metadata about files (author, title, etc) to the 'params' variable
     // of the Dropzone in the format { <filename> : {metadata as dict} }. 
     var formData = {};
     $(".dz-preview").each(function(k, v){
         var file_name = $(".dz-filename", $(this)).find('span').html();                                 
         var speaker_name= $('.presentation-speaker-name', $(this)).find('input').val();
         var presentation_title= $('.presentation-title', $(this)).find('input').val();
         var presentation_name= $('.presentation-name', $(this)).find('input').val();    
         var presentation_description= $('.presentation-description', $(this)).find('textarea').val();
         
         var meetup_id= $('#hidden_field_for_meetup_id').html();  
               
         console.log(file_name + speaker_name + presentation_title + presentation_description);
         formData[file_name] =  JSON.stringify({"speaker_name":speaker_name, 
                                                "presentation_title": presentation_title, 
                                                "presentation_description": presentation_description,
                                                "meetup_id": meetup_id });                                                    
     }); 
     return formData;                                  
                                      
    }
};

Dropzone.options.myAwesomeDropzone= {
  autoProcessQueue: false,
  addRemoveLinks: true,
  
  previewTemplate: ['',
                '<div class="dz-preview dz-file-preview">',
                   '<div class="dz-details">',
                      '<div class="dz-filename"><span data-dz-name></span></div>',
                      '<div class="dz-size" data-dz-size></div>',
                      '<img data-dz-thumbnail />',
                   '</div>',
                   '<div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>',
                   '<div class="dz-success-mark"><span>✔</span></div>',
                   '<div class="dz-error-mark"><span>✘</span></div>',
                   '<div class="dz-error-message"><span data-dz-errormessage></span></div>',                  
                   '<div class="presentation-speaker-name presentation-details validate-speaker">',
                       '<input class="form-control" id="focusedInput" type="text" value="Speaker Name">',
                   '</div>',
                   '<div class="presentation-title validate-title presentation-details">',
                       '<input class="form-control" id="focusedInput" type="text" value="Presentation title">',
                   '</div>',                   
                   '<div class="presentation-description validate-description presentation-details">',
                       '<textarea class="form-control" rows="3" id="textArea">A brief description of the talk.</textarea>',
                   '</div>',
                '</div>'].join('\n'),
                                       
  init: function() {
    var myDropzone = this;
    
    // First change the button to actually tell Dropzone to process the queue.
    this.element.querySelector("button[type=submit]").addEventListener("click", function(e) {
      // Make sure that the form isn't actually being sent.
      e.preventDefault();
      e.stopPropagation();
      
      // Add all metadata about each file into each post request      
      // updated_form_data = MeetupSlides.generateFormDataParams();
      //this.params = MeetupSlides.generateFormDataParams();
      
      
      var validation_succeeded = MeetupSlides.validateUpload();
      
      if (validation_succeeded == true){
                                         
         myDropzone.processQueue();                                         
      }else{
            alert("Please fill in the boxes marked with red. Thanks! It helps us keep our data clean.");
      }
      
    });
    
    this.on("complete", function() {
      if (this.getQueuedFiles().length == 0 && this.getUploadingFiles().length == 0) {
        // File finished uploading, and there aren't any left in the queue.
        //alert("alright buddy");
        var uploaded_files = [];        
        for(i=0; i < this.files.length;i++){
          if (this.files[i].accepted == true){
            //uploaded_files.append(this.files[i].name);            
          }
        }    
      }
    });
                                     
    this.on("sending", function(file, xhr, formdata){
        additional_form_data =  MeetupSlides.generateFormDataParams();                                                    
        key = "metadata"
        value = additional_form_data[file.name];
        formdata.append(key, value);
        console.log("do something here and add additional fields");                                       
    });                                     
  }
};