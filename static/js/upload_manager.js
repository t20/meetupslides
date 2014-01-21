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
        title_validation = MeetupSlides.textValidator('.validate-title', 'input', 'Presentation title');
        description_validation = MeetupSlides.textValidator('.validate-description', 'textarea', 'A brief description of the talk.');
                
        if (speaker_validation == true  && title_validation == true && description_validation == true){
           return true;    
        }else{
           return false;
        }                                                                                                 
    },
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
      var validation_succeeded = MeetupSlides.validateUpload();
      
      if (validation_succeeded == true ){
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
            uploaded_files.append(this.files[i].name);
            
          }
        }    
      }
    });
                                     
    this.on("sending", function(xhr, formdata){
        console.log("do something here and add additional fields");                                       
    });                                     
  }
};