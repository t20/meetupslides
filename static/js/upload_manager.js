Dropzone.options.myDrop = {
  init: function() {
    this.on("complete", function() {
      if (this.getQueuedFiles().length == 0 && this.getUploadingFiles().length == 0) {
        // File finished uploading, and there aren't any left in the queue.
        alert("alright buddy");
      }
    });
  }
};