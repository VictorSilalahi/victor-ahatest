function Save() {
    if (document.getElementById("txtEmailMail").value=='') {
        alert("Input your email address!");
        document.getElementById("txtEmailMail").focus();
        return false;
    }
    if (document.getElementById("txtPasswordMail").value=='') {
        alert("Input your password!");
        document.getElementById("txtPasswordMail").focus();
        return false;
    }
    if (document.getElementById("txtEmailGoauth").value=='') {
        alert("Input your email address!");
        document.getElementById("txtEmailGoauth").focus();
        return false;
    }
    if (document.getElementById("txtPasswordGoauth").value=='') {
        alert("Input your password!");
        document.getElementById("txtPasswordGoauth").focus();
        return false;
    }
    if (document.getElementById("txtEmailSignUp").value=='') {
        alert("Input your password!");
        document.getElementById("txtEmailSignUp").focus();
        return false;
    }
    if (document.getElementById("txtPasswordSignUp").value=='') {
        alert("Input your password!");
        document.getElementById("txtPasswordSignUp").focus();
        return false;
    }
    if (document.getElementById("txtPasswordSignUpV").value=='') {
        alert("Input your password for Verification!");
        document.getElementById("txtPasswordSignUpV").focus();
        return false;
    }
    document.getElementById("frmMailGoauth").submit();

}

