//AUTOR: Timo Eisert (7470259)

//initializes graphs at the start
function initiatePage(){ 
    
    getProgress();
    getTokens();
    getPOS();
    getSentiment();
    getNamedentities();
    getSpeakers();
    getProtocols();   
    
}

// This function gets the progress data from the database (For the progress bar in the top right corner)
function getProgress(){
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/progress",
                      			
            success: function(data){
                if (data["success"] == "true"){
                    var already_processed = parseInt(data["current"]);
                    var total = parseInt(data["total"]);

                    var percentage = Math.floor(((already_processed / total) * 100))
                    var progressbar = document.getElementById("progressbar1");
                   
                    progressbar.innerHTML = percentage + "%"
                    progressbar.style = "width: " + percentage + "%"

                }
                else{
                    console.log("ERROR");
                }           
                
            },
            error: function (xhr, ajaxOptions, thrownError){
                console.log("ERROR (" + xhr.status + ")");
                
            }
        });					
    });        
}

// This function gets the token data from the database
function getTokens(){
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/tokens",
                      			
            success: function(data){
                if (data["success"] == "true"){
                    var token_list = data["result"];
                    var token_name = [];
                    var token_amount = [];
                                           
                    for(var i = 0; i < 50; i++){
                        token_name.push(token_list[i]["token"]);
                        token_amount.push(token_list[i]["count"]);
                    }

                    updateTokenLineChart(token_name, token_amount);
                  
                }
                else{
                    console.log("ERROR");
                }           
                
            },
            error: function (xhr, ajaxOptions, thrownError){
                console.log("ERROR (" + xhr.status + ")");                
            }
        });					
    });        
}

// This function gets the POS data from the database
function getPOS(){
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/pos",
                     			
            success: function(data){
                if (data["success"] == "true"){
                    var pos_list = data["result"];
                    var pos_names = [];
                    var pos_values = [];
                    
                        
                    for(var i = 0; i < pos_list.length; i++){
                        pos_names.push(pos_list[i]["POS"]);
                        pos_values.push(pos_list[i]["count"]);
                    }

                    updatePosBarChart(pos_names, pos_values);
                  
                }
                else{
                    console.log("ERROR");
                }           
                
            },
            error: function (xhr, ajaxOptions, thrownError){
                console.log("ERROR (" + xhr.status + ")");
                
            }
        });					
    });        
}

// This function gets the sentiment data from the database
function getSentiment(){
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/sentiment",	

            success: function(data){
                
                if (data["success"] == "true"){
                    var sentimentcounter = [0,0,0];
                    var sentiment_list = data["result"];
                    
                    
                    for(var i = 0; i < sentiment_list.length; i++) {
                        var curr_sentiment = parseFloat(sentiment_list[i]["sentiment"]);
                        var curr_count = sentiment_list[i]["count"];
                        

                        if(curr_sentiment > 0){
                            sentimentcounter[0] += curr_count;
                        }
                        else if(curr_sentiment === 0){
                            
                            sentimentcounter[1] += curr_count;    
                        }
                        else{
                            sentimentcounter[2] += curr_count;   
                        }
                    }
                    
                    updateSentimentRadarChart(sentimentcounter);
                  
                }
                else{
                    console.log("ERROR");
                }
            },
            error: function (error){
                console.log("ERROR");
            }
        });			
    });    
}

// This function gets the namedentity data from the database
function getNamedentities(){
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/namedEntities",	

            success: function(data){
                
                if (data["success"] == "true"){
                    var namedentitylist = data["result"];

                    var person_list = namedentitylist[0]["persons"];
                    var organisation_list = namedentitylist[1]["organisations"];
                    var location_list = namedentitylist[2]["locations"];
                    
                    

                    var label_list = [[],[],[]]
                    var count_list = [[],[],[]]

                    for(var i = 0; i < 50; i++){
                        label_list[0].push(location_list[i]["element"]);
                        label_list[1].push(organisation_list[i]["element"]); 
                        label_list[2].push(person_list[i]["element"]);

                        count_list[0].push(location_list[i]["count"]);                       
                        count_list[1].push(organisation_list[i]["count"]);
                        count_list[2].push(person_list[i]["count"]);
                    }
                    
                    updateNamedEntLineChart(label_list,count_list);                                  
                                   
                }
                else{
                    console.log("ERROR");
                }
            },
            error: function (error){
                console.log("ERROR");
            }
        });			
    });    
}

// This function gets the speaker data from the database
function getSpeakers(){
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/speaker",	

            success: function(data){

                if (data["success"] == "true"){
                    var speakerlist = data["result"];
                    
                    var idlist = []
                    var namelist = []
                    var urllist = []
                    var speechcount = []

                    speakerlist.sort(function(a,b){return (b["rede"].length) - (a["rede"].length)})

                    for(var i = 0; i < 50; i++){
                        idlist.push(speakerlist[i]["_id"]);
                        namelist.push(speakerlist[i]["vorname"]+" "+speakerlist[i]["nachname"]);
                        urllist.push(speakerlist[i]["linkzubild"]);
                        speechcount.push((speakerlist[i]["rede"]).length);
                    }
                                     
                    
                    updateSpeakerBarChart(idlist, namelist, speechcount, urllist);                   
                  
                }
                else{
                    console.log("ERROR");
                }

            },
            error: function (error){
                console.log("ERROR");
            }
        });			
    });    
}


// This function gets the protocol data from the database (For the speech selection)
function getProtocols(){
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/protocol",	

            success: function(data){

                if (data["success"] == "true"){
                    var tempprotocollist = data["ids"];
                    
                    // tempprotocollist contains all protocol ids
                    createProtocolSelect(tempprotocollist);                    
                  
                }
                else{
                    console.log("ERROR");
                }
                
            },
            error: function (error){
                console.log("ERROR");
            }
        });			
    });        
}

// This function gets the agendaitem data from the database (For the speech selection)
function getAgendaitems(protocolid){
    var select2 = document.getElementById("select2");

    var i, L = select2.options.length - 1;
    for(i = L; i >= 0; i--) {
      select2.remove(i);
    }

    var select3 = document.getElementById("select3");

    var i, L = select3.options.length - 1;
    for(i = L; i >= 0; i--) {
      select3.remove(i);
    }
    
    console.log(protocolid)
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/protocol/" + protocolid,	

            success: function(data){
                            
                var tempprotocol = data["tagesordnungen"]
                var agendaitemlist = []
                
                for(var i = 0; i < tempprotocol.length; i++){
                    agendaitemlist.push(tempprotocol[i]["_id"]);
                }
                
                // agendaitemlist contains all agendaitems of the protocol (at protocolid)
                createAgendaSelect(agendaitemlist, protocolid)
                            
            },
            error: function (error){
                console.log("ERROR");
            }
        });			
    });        
}

// This function gets the speech data from the database (For the speech selection)
function getSpeeches(agendaid, protocolid ){
    var select3 = document.getElementById("select3");

    var i, L = select3.options.length - 1;
    for(i = L; i >= 0; i--) {
      select3.remove(i);
    }
        
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/protocol/" + protocolid,	

            success: function(data){

                var tempprotocol = data["tagesordnungen"]
                var curr_protocol = tempprotocol.find(item => item._id === agendaid);                              
                var speechlist = curr_protocol.rede;
                
                // speechlist contains all speeches of a specific agendaitem (of a specific protocol)
                createSpeechSelect(speechlist, protocolid);
                                
            },
            error: function (error){
                console.log("ERROR");
            }
        });			
    });       
}

// This function gets the speech text from the database (For the speech selection)
function getSpeechText(speechid){
    $(function(){
		$.ajax({
			method: "GET",
            dataType: "json",
			url: "http://localhost:4567/speech/" + speechid,	

            success: function(data){

                var paragraphs = data["paragraphs:"]
                var text = paragraphs.join('')
                
                // text contains the actual text of specific speech
                insertSpeech(text);
                               
            },
            error: function (error){
                console.log("ERROR");
            }
        });			
    });    
}