<script type="text/javascript">
var count = "10";  
function limiter(){
var tex = document.myform.comment.value;
var len = tex.length;
if(len > count){
        tex = tex.substring(0,count);
        document.myform.content.value =tex;
        return false;
}
document.myform.limit.value = count-len;
}
</script>
