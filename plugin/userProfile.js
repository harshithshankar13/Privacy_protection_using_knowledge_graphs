$(document).ready(function(){
    var idEduIndex = 0;
    var idProIndex = 0;
    // save user detail to browser storage ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    $("button.submitUserInfo").click(function(){
        // get basic details
        var userName = document.getElementById("userName").value.toLowerCase() ;
        var profession = document.getElementById("profession").value.toLowerCase() ;
        var nationality = document.getElementById("Nationality").value.toLowerCase() ;
        var DOB = document.getElementById("DOB").value ;

        // get education details
        var educationDetails =  []
        for (i = 0; i < idEduIndex; i++)
        {
            var singleEdu = {};
            singleEdu["InstitutionName"] = document.getElementById("instTextBox" + i).value.toLowerCase() ;
            singleEdu["DegreeObtained"] = document.getElementById("degreeTextBox" + i).value.toLowerCase() ;
            singleEdu["InstituteURL"] = document.getElementById("instituteURLTextBox" + i).value.toLowerCase() ;
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
            singleProf["CompanyName"] = document.getElementById("compTextBox" + i).value.toLowerCase() ;
            singleProf["Role"] = document.getElementById("positionTextBox" + i).value.toLowerCase() ;
            singleProf["CompanyURL"] = document.getElementById("companyURLTextBox" + i).value.toLowerCase() ;
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
        div2.setAttribute('id','oneEducation');

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

        var instituteURLLabel = document.createElement("label");
        instituteURLLabel.innerHTML = "Institute's website URL: ";

        var instituteURLTextBox = document.createElement("INPUT");
        instituteURLTextBox.setAttribute("type", "text");
        instituteURLTextBox.setAttribute("id", "instituteURLTextBox" + idEduIndex);

        var locLabel = document.createElement("label");
        locLabel.innerHTML = "Location : ";

        // var locTextBox = document.createElement("INPUT");
        // locTextBox.setAttribute("type", "text");
        // locTextBox.setAttribute("id", "locTextBox" + idEduIndex);

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
        var brk6 = document.createElement("br")

        document.getElementById("education").appendChild(div2);
 
        div2.appendChild(instLabel);
        div2.appendChild(instTextBox);
        div2.appendChild(brk1);

        div2.appendChild(degreeLabel);
        div2.appendChild(degreeTextBox);
        div2.appendChild(brk2);

        div2.appendChild(instituteURLLabel);
        div2.appendChild(instituteURLTextBox);
        div2.appendChild(brk6);

        div2.appendChild(locLabel);
        div2.insertAdjacentHTML('beforeend', '<select id="locTextBox' + idEduIndex + '" data-fillr="bound" autocomplete="on"><option value=""></option><option >Afghanistan</option><option >Åland</option><option >Albania</option><option >Algeria</option><option >American Samoa</option><option >Andorra</option><option >Angola</option><option >Anguilla</option><option >Antarctica</option><option >Antigua and Barbuda</option><option >Argentina</option><option >Armenia</option><option >Aruba</option><option >Australia</option><option >Austria</option><option >Azerbaijan</option><option >Bahamas</option><option >Bahrain</option><option >Bangladesh</option><option >Barbados</option><option >Belarus</option><option >Belgium</option><option >Belize</option><option >Benin</option><option >Bermuda</option><option >Bhutan</option><option >Bolivia</option><option >Bonaire, Sint Eustatius, and Saba</option><option >Bosnia and Herzegovina</option><option >Botswana</option><option >Bouvet Island</option><option >Brazil</option><option >British Indian Ocean Territory</option><option >British Virgin Islands</option><option >Brunei</option><option >Bulgaria</option><option >Burkina Faso</option><option >Burundi</option><option >Cabo Verde</option><option >Cambodia</option><option >Cameroon</option><option >Canada</option><option >Cayman Islands</option><option >Central African Republic</option><option >Chad</option><option >Chile</option><option >China</option><option >Christmas Island</option><option >Cocos [Keeling] Islands</option><option >Colombia</option><option >Comoros</option><option >Congo Republic</option><option >Cook Islands</option><option >Costa Rica</option><option >Croatia</option><option >Cuba</option><option >Curaçao</option><option >Cyprus</option><option >Czechia</option><option >Denmark</option><option >Djibouti</option><option >Dominica</option><option >Dominican Republic</option><option >DR Congo</option><option >Ecuador</option><option >Egypt</option><option >El Salvador</option><option >Equatorial Guinea</option><option >Eritrea</option><option >Estonia</option><option >Eswatini</option><option >Ethiopia</option><option >Falkland Islands</option><option >Faroe Islands</option><option >Fiji</option><option >Finland</option><option >France</option><option >French Guiana</option><option >French Polynesia</option><option >French Southern Territories</option><option >Gabon</option><option >Gambia</option><option >Georgia</option><option >Germany</option><option >Ghana</option><option >Gibraltar</option><option >Greece</option><option >Greenland</option><option >Grenada</option><option >Guadeloupe</option><option >Guam</option><option >Guatemala</option><option >Guernsey</option><option >Guinea</option><option >Guinea-Bissau</option><option >Guyana</option><option >Haiti</option><option >Heard Island and McDonald Islands</option><option >Honduras</option><option >Hong Kong</option><option >Hungary</option><option >Iceland</option><option >India</option><option >Indonesia</option><option >Iran</option><option >Iraq</option><option >Ireland</option><option >Isle of Man</option><option >Israel</option><option >Italy</option><option >Ivory Coast</option><option >Jamaica</option><option >Japan</option><option >Jersey</option><option >Jordan</option><option >Kazakhstan</option><option >Kenya</option><option >Kiribati</option><option >Kosovo</option><option >Kuwait</option><option >Kyrgyzstan</option><option >Laos</option><option >Latvia</option><option >Lebanon</option><option >Lesotho</option><option >Liberia</option><option >Libya</option><option >Liechtenstein</option><option >Lithuania</option><option >Luxembourg</option><option >Macao</option><option >Madagascar</option><option >Malawi</option><option >Malaysia</option><option >Maldives</option><option >Mali</option><option >Malta</option><option >Marshall Islands</option><option >Martinique</option><option >Mauritania</option><option >Mauritius</option><option >Mayotte</option><option >Mexico</option><option >Micronesia</option><option >Moldova</option><option >Monaco</option><option >Mongolia</option><option >Montenegro</option><option >Montserrat</option><option >Morocco</option><option >Mozambique</option><option >Myanmar</option><option >Namibia</option><option >Nauru</option><option >Nepal</option><option >Netherlands</option><option >New Caledonia</option><option >New Zealand</option><option >Nicaragua</option><option >Niger</option><option >Nigeria</option><option >Niue</option><option >Norfolk Island</option><option >North Korea</option><option >North Macedonia</option><option >Northern Mariana Islands</option><option >Norway</option><option >Oman</option><option >Pakistan</option><option >Palau</option><option >Palestine</option><option >Panama</option><option >Papua New Guinea</option><option >Paraguay</option><option >Peru</option><option >Philippines</option><option >Pitcairn Islands</option><option >Poland</option><option >Portugal</option><option >Puerto Rico</option><option >Qatar</option><option >Réunion</option><option >Romania</option><option >Russia</option><option >Rwanda</option><option >Saint Barthélemy</option><option >Saint Helena</option><option >Saint Lucia</option><option >Saint Martin</option><option >Saint Pierre and Miquelon</option><option >Samoa</option><option>San Marino</option><option >São Tomé and Príncipe</option><option >Saudi Arabia</option><option >Senegal</option><option >Serbia</option><option >Seychelles</option><option >Sierra Leone</option><option >Singapore</option><option >Sint Maarten</option><option >Slovakia</option><option >Slovenia</option><option >Solomon Islands</option><option >Somalia</option><option >South Africa</option><option >South Georgia and South Sandwich Islands</option><option >South Korea</option><option >South Sudan</option><option >Spain</option><option >Sri Lanka</option><option >St Kitts and Nevis</option><option >St Vincent and Grenadines</option><option >Sudan</option><option >Suriname</option><option >Svalbard and Jan Mayen</option><option >Sweden</option><option >Switzerland</option><option >Syria</option><option >Taiwan</option><option >Tajikistan</option><option >Tanzania</option><option >Thailand</option><option >Timor-Leste</option><option >Togo</option><option >Tokelau</option><option >Tonga</option><option >Trinidad and Tobago</option><option >Tunisia</option><option >Turkey</option><option >Turkmenistan</option><option >Turks and Caicos Islands</option><option >Tuvalu</option><option >U.S. Minor Outlying Islands</option><option >U.S. Virgin Islands</option><option >Uganda</option><option >Ukraine</option><option >United Arab Emirates</option><option >United Kingdom</option><option >United States</option><option >Uruguay</option><option >Uzbekistan</option><option >Vanuatu</option><option >Vatican City</option><option >Venezuela</option><option >Vietnam</option><option >Wallis and Futuna</option><option >Western Sahara</option><option >Yemen</option><option >Zambia</option><option >Zimbabwe</option></select>');
        div2.appendChild(brk3);

        div2.appendChild(eduFrom);
        div2.appendChild(eduMid);
        div2.appendChild(eduTill);
        div2.appendChild(brk4);

        // div2.appendChild(removeEdu);
        div2.appendChild(brk5);

        idEduIndex++;
    });

    // addProfession 
    $("button.addProfession").click(function(){

        var div1 =document.createElement('div');
        div1.setAttribute('id','oneExpirence');

        var compLabel = document.createElement("label");
        compLabel.innerHTML = "Company Name : ";

        var compTextBox = document.createElement("INPUT");
        compTextBox.setAttribute("type", "text");
        compTextBox.setAttribute("id", "compTextBox" + idProIndex);

        var companyURLLabel = document.createElement("label");
        companyURLLabel.innerHTML = "Company's website URL: ";

        var companyURLTextBox = document.createElement("INPUT");
        companyURLTextBox.setAttribute("type", "text");
        companyURLTextBox.setAttribute("id", "companyURLTextBox" + idProIndex);

        var positionLabel = document.createElement("label");
        positionLabel.innerHTML = "Role : ";

        var positionTextBox = document.createElement("INPUT");
        positionTextBox.setAttribute("type", "text");
        positionTextBox.setAttribute("id", "positionTextBox" + idProIndex);

        var locLabel = document.createElement('label');
        locLabel.innerHTML = "Location : ";

        // var locTextBox = document.createElement("INPUT");
        // locTextBox.setAttribute("type", "text");
        // locTextBox.setAttribute("id", "locTextBox" + idProIndex);

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
        removePro.setAttribute("id","removePro" + idProIndex);
        removePro.setAttribute("style", "text-align:center;")

        var brk1 = document.createElement("br")
        var brk2 = document.createElement("br")
        var brk3 = document.createElement("br")
        var brk4 = document.createElement("br")
        var brk5 = document.createElement("br")
        var brk6 = document.createElement("br")
 
        document.getElementById("Professional_experience").appendChild(div1);
        
        div1.appendChild(compLabel);
        div1.appendChild(compTextBox);
        div1.appendChild(brk1);

        div1.appendChild(positionLabel);
        div1.appendChild(positionTextBox);
        div1.appendChild(brk2);

        div1.appendChild(companyURLLabel);
        div1.appendChild(companyURLTextBox);
        div1.appendChild(brk6);

        div1.appendChild(locLabel);
        div1.insertAdjacentHTML('beforeend', '<select id="locTextBox' + idEduIndex + '" data-fillr="bound" autocomplete="on"><option value=""></option><option >Afghanistan</option><option >Åland</option><option >Albania</option><option >Algeria</option><option >American Samoa</option><option >Andorra</option><option >Angola</option><option >Anguilla</option><option >Antarctica</option><option >Antigua and Barbuda</option><option >Argentina</option><option >Armenia</option><option >Aruba</option><option >Australia</option><option >Austria</option><option >Azerbaijan</option><option >Bahamas</option><option >Bahrain</option><option >Bangladesh</option><option >Barbados</option><option >Belarus</option><option >Belgium</option><option >Belize</option><option >Benin</option><option >Bermuda</option><option >Bhutan</option><option >Bolivia</option><option >Bonaire, Sint Eustatius, and Saba</option><option >Bosnia and Herzegovina</option><option >Botswana</option><option >Bouvet Island</option><option >Brazil</option><option >British Indian Ocean Territory</option><option >British Virgin Islands</option><option >Brunei</option><option >Bulgaria</option><option >Burkina Faso</option><option >Burundi</option><option >Cabo Verde</option><option >Cambodia</option><option >Cameroon</option><option >Canada</option><option >Cayman Islands</option><option >Central African Republic</option><option >Chad</option><option >Chile</option><option >China</option><option >Christmas Island</option><option >Cocos [Keeling] Islands</option><option >Colombia</option><option >Comoros</option><option >Congo Republic</option><option >Cook Islands</option><option >Costa Rica</option><option >Croatia</option><option >Cuba</option><option >Curaçao</option><option >Cyprus</option><option >Czechia</option><option >Denmark</option><option >Djibouti</option><option >Dominica</option><option >Dominican Republic</option><option >DR Congo</option><option >Ecuador</option><option >Egypt</option><option >El Salvador</option><option >Equatorial Guinea</option><option >Eritrea</option><option >Estonia</option><option >Eswatini</option><option >Ethiopia</option><option >Falkland Islands</option><option >Faroe Islands</option><option >Fiji</option><option >Finland</option><option >France</option><option >French Guiana</option><option >French Polynesia</option><option >French Southern Territories</option><option >Gabon</option><option >Gambia</option><option >Georgia</option><option >Germany</option><option >Ghana</option><option >Gibraltar</option><option >Greece</option><option >Greenland</option><option >Grenada</option><option >Guadeloupe</option><option >Guam</option><option >Guatemala</option><option >Guernsey</option><option >Guinea</option><option >Guinea-Bissau</option><option >Guyana</option><option >Haiti</option><option >Heard Island and McDonald Islands</option><option >Honduras</option><option >Hong Kong</option><option >Hungary</option><option >Iceland</option><option >India</option><option >Indonesia</option><option >Iran</option><option >Iraq</option><option >Ireland</option><option >Isle of Man</option><option >Israel</option><option >Italy</option><option >Ivory Coast</option><option >Jamaica</option><option >Japan</option><option >Jersey</option><option >Jordan</option><option >Kazakhstan</option><option >Kenya</option><option >Kiribati</option><option >Kosovo</option><option >Kuwait</option><option >Kyrgyzstan</option><option >Laos</option><option >Latvia</option><option >Lebanon</option><option >Lesotho</option><option >Liberia</option><option >Libya</option><option >Liechtenstein</option><option >Lithuania</option><option >Luxembourg</option><option >Macao</option><option >Madagascar</option><option >Malawi</option><option >Malaysia</option><option >Maldives</option><option >Mali</option><option >Malta</option><option >Marshall Islands</option><option >Martinique</option><option >Mauritania</option><option >Mauritius</option><option >Mayotte</option><option >Mexico</option><option >Micronesia</option><option >Moldova</option><option >Monaco</option><option >Mongolia</option><option >Montenegro</option><option >Montserrat</option><option >Morocco</option><option >Mozambique</option><option >Myanmar</option><option >Namibia</option><option >Nauru</option><option >Nepal</option><option >Netherlands</option><option >New Caledonia</option><option >New Zealand</option><option >Nicaragua</option><option >Niger</option><option >Nigeria</option><option >Niue</option><option >Norfolk Island</option><option >North Korea</option><option >North Macedonia</option><option >Northern Mariana Islands</option><option >Norway</option><option >Oman</option><option >Pakistan</option><option >Palau</option><option >Palestine</option><option >Panama</option><option >Papua New Guinea</option><option >Paraguay</option><option >Peru</option><option >Philippines</option><option >Pitcairn Islands</option><option >Poland</option><option >Portugal</option><option >Puerto Rico</option><option >Qatar</option><option >Réunion</option><option >Romania</option><option >Russia</option><option >Rwanda</option><option >Saint Barthélemy</option><option >Saint Helena</option><option >Saint Lucia</option><option >Saint Martin</option><option >Saint Pierre and Miquelon</option><option >Samoa</option><option>San Marino</option><option >São Tomé and Príncipe</option><option >Saudi Arabia</option><option >Senegal</option><option >Serbia</option><option >Seychelles</option><option >Sierra Leone</option><option >Singapore</option><option >Sint Maarten</option><option >Slovakia</option><option >Slovenia</option><option >Solomon Islands</option><option >Somalia</option><option >South Africa</option><option >South Georgia and South Sandwich Islands</option><option >South Korea</option><option >South Sudan</option><option >Spain</option><option >Sri Lanka</option><option >St Kitts and Nevis</option><option >St Vincent and Grenadines</option><option >Sudan</option><option >Suriname</option><option >Svalbard and Jan Mayen</option><option >Sweden</option><option >Switzerland</option><option >Syria</option><option >Taiwan</option><option >Tajikistan</option><option >Tanzania</option><option >Thailand</option><option >Timor-Leste</option><option >Togo</option><option >Tokelau</option><option >Tonga</option><option >Trinidad and Tobago</option><option >Tunisia</option><option >Turkey</option><option >Turkmenistan</option><option >Turks and Caicos Islands</option><option >Tuvalu</option><option >U.S. Minor Outlying Islands</option><option >U.S. Virgin Islands</option><option >Uganda</option><option >Ukraine</option><option >United Arab Emirates</option><option >United Kingdom</option><option >United States</option><option >Uruguay</option><option >Uzbekistan</option><option >Vanuatu</option><option >Vatican City</option><option >Venezuela</option><option >Vietnam</option><option >Wallis and Futuna</option><option >Western Sahara</option><option >Yemen</option><option >Zambia</option><option >Zimbabwe</option></select>');
        div1.appendChild(brk3);
        
        div1.appendChild(From);
        div1.appendChild(Mid);
        div1.appendChild(Till);
        div1.appendChild(brk4);

        // div1.appendChild(removePro);
        div1.appendChild(brk5);

        idProIndex ++;
    });

    $("#country").jeoCountrySelect({
        callback: function () {
            $("#country").removeAttr('disabled');
        }
    });
    
    $("#city").jeoCityAutoComplete();
});

