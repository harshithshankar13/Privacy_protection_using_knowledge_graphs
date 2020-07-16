$(document).ready(function(){
    var idEduIndex = 0;
    var idProIndex = 0;
    // save user detail to browser storage ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    $("button.submitUserInfo").click(function(){
        // get basic details
        var userName = document.getElementById("userName").value ;
        var profession = document.getElementById("profession").value ;
        var nationality = document.getElementById("Nationality").value ;
        var DOB = document.getElementById("DOB").value ;

        // get education details
        var educationDetails =  []
        for (i = 0; i < idEduIndex; i++)
        {
            var singleEdu = {};
            singleEdu["InstitutionName"] = document.getElementById("instTextBox" + i).value ;
            singleEdu["DegreeObtained"] = document.getElementById("degreeTextBox" + i).value ;
            singleEdu["Location"] = document.getElementById("locTextBox" + i).value ;
            singleEdu["StudiedFrom"] = document.getElementById("eduFrom" + i).value ;
            singleEdu["StudiedTill"] = document.getElementById("eduTill" + i).value ;

            educationDetails.push(singleEdu);
        }

        // get education details
        var experienceDetails =  []
        for (i = 0; i < idProIndex; i++)
        {
            var singleProf = {};
            singleProf["CompanyName"] = document.getElementById("compTextBox" + i).value ;
            singleProf["Role"] = document.getElementById("positionTextBox" + i).value ;
            singleProf["Location"] = document.getElementById("locTextBox" + i).value ;
            singleProf["WorkedFrom"] = document.getElementById("fromPro" + i).value ;
            singleProf["WorkedTill"] = document.getElementById("tillPro" + i).value ;

            experienceDetails.push(singleProf);
        }

       // store user profile/graph into local browser storage
        chrome.storage.sync.set({'userName': userName, 
        "nationality":nationality,
        "profession": profession,
        "DOB": DOB,
        "EducationDetails": educationDetails,
        "ProfessionalExpirenceDetails": experienceDetails}, 
        function() {
            console.log('Value is set to value');
        });
    });
    // ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    // addEducation 
    $("button.addEducation").click(function(){
        var div2 =document.createElement('div');
        div2.setAttribute('id','oneEducation' + idEduIndex);

        var instLabel = document.createElement("label");
        instLabel.innerHTML = "Institution name : ";

        var instTextBox = document.createElement("INPUT");
        instTextBox.setAttribute("type", "text");
        instTextBox.setAttribute("id", "instTextBox" + idEduIndex);

        var degreeLabel = document.createElement("label");
        degreeLabel.innerHTML = "Degree obtained : ";

        var degreeTextBox = document.createElement("INPUT");
        degreeTextBox.setAttribute("type", "text");
        degreeTextBox.setAttribute("id", "degreeTextBox" + idEduIndex);

        var locLabel = document.createElement("label");
        locLabel.innerHTML = "Location : ";

        var locTextBox = document.createElement("INPUT");
        locTextBox.setAttribute("type", "text");
        locTextBox.setAttribute("id", "locTextBox" + idEduIndex);

        var eduFrom = document.createElement("INPUT");
        eduFrom.setAttribute("type", "date");
        eduFrom.setAttribute("id", "eduFrom" + idEduIndex);

        var eduMid = document.createElement("label");
        eduMid.innerHTML = " To ";
        eduMid.setAttribute("style", "text-align:center;")

        var eduTill = document.createElement("INPUT");
        eduTill.setAttribute("type", "date");
        eduTill.setAttribute("id", "eduTill" + idEduIndex);

        var removeEdu = document.createElement("button");
        removeEdu.innerHTML = "Delete";
        removeEdu.setAttribute("id","removeEdu");
        removeEdu.setAttribute("style", "text-align:center;")

        var brk1 = document.createElement("br")
        var brk2 = document.createElement("br")
        var brk3 = document.createElement("br")
        var brk4 = document.createElement("br")
        var brk5 = document.createElement("br")

        document.getElementById("education").appendChild(div2);
 
        div2.appendChild(instLabel);
        div2.appendChild(instTextBox);
        div2.appendChild(brk1);

        div2.appendChild(degreeLabel);
        div2.appendChild(degreeTextBox);
        div2.appendChild(brk2);

        div2.appendChild(locLabel);
        div2.appendChild(locTextBox);
        div2.appendChild(brk3);

        div2.appendChild(eduFrom);
        div2.appendChild(eduMid);
        div2.appendChild(eduTill);
        div2.appendChild(brk4);

        div2.appendChild(removeEdu);
        div2.appendChild(brk5);

        idEduIndex++;
    });

    // addEducation 
    $("button.addProfession").click(function(){

        var div1 =document.createElement('div');
        div1.setAttribute('id','oneExpirence');

        var compLabel = document.createElement("label");
        compLabel.innerHTML = "Company Name : ";

        var compTextBox = document.createElement("INPUT");
        compTextBox.setAttribute("type", "text");
        compTextBox.setAttribute("id", "compTextBox" + idProIndex);

        var positionLabel = document.createElement("label");
        positionLabel.innerHTML = "Role : ";

        var positionTextBox = document.createElement("INPUT");
        positionTextBox.setAttribute("type", "text");
        positionTextBox.setAttribute("id", "positionTextBox" + idProIndex);

        var locLabel = document.createElement("label");
        locLabel.innerHTML = "Location : ";

        var locTextBox = document.createElement("INPUT");
        locTextBox.setAttribute("type", "text");
        locTextBox.setAttribute("id", "locTextBox" + idProIndex);

        var From = document.createElement("INPUT");
        From.setAttribute("type", "date");
        From.setAttribute("id", "fromPro" + idProIndex);

        var Mid = document.createElement("label");
        Mid.innerHTML = " To ";
        Mid.setAttribute("id","midPro");
        Mid.setAttribute("style", "text-align:center;")

        var Till = document.createElement("INPUT");
        Till.setAttribute("type", "date");
        Till.setAttribute("id", "tillPro" + idProIndex);

        var removePro = document.createElement("button");
        removePro.innerHTML = "Delete";
        removePro.setAttribute("id","removePro");
        removePro.setAttribute("style", "text-align:center;")

        var brk1 = document.createElement("br")
        var brk2 = document.createElement("br")
        var brk3 = document.createElement("br")
        var brk4 = document.createElement("br")
        var brk5 = document.createElement("br")
 
        document.getElementById("Professional_experience").appendChild(div1);
        
        div1.appendChild(compLabel);
        div1.appendChild(compTextBox);
        div1.appendChild(brk1);

        div1.appendChild(positionLabel);
        div1.appendChild(positionTextBox);
        div1.appendChild(brk2);

        div1.appendChild(locLabel);
        div1.appendChild(locTextBox);
        div1.appendChild(brk3);
        
        div1.appendChild(From);
        div1.appendChild(Mid);
        div1.appendChild(Till);
        div1.appendChild(brk4);

        div1.appendChild(removePro);
        div1.appendChild(brk5);

        idProIndex ++;
    });
});