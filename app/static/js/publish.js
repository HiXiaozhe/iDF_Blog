var currentCommentButton = null;

function publishPost() {
    var activeTextAraeID = '#home_textarea';
    var inputText = $(activeTextAraeID).val();
    console.log(inputText);
    // 获得这个标签页的文本框的内容
    $(activeTextAraeID).val('');
    // 清空这个标签页的文本框的内容
    console.log(' 中输入的内容：', inputText);
    addPostToPage(inputText);
    // document.getElementById('postText').value = '';
    // const postText = document.getElementById('postText').value;
}

function addPostToPage(text) {
	var picid = localStorage.getItem("randompic");
	var picsrc = "img/p"+picid+".png";
    var firstPost = $('#mainContent .osahan-post:eq(0)');
    var newPost = `
    <div class="box shadow-sm border rounded bg-white mb-3 osahan-post">
        <div class="p-3 d-flex align-items-center border-bottom osahan-post-header">
            <div class="dropdown-list-image mr-3">
                <img class="rounded-circle" src=`+ picsrc +` alt="">
                <div class="status-indicator bg-success"></div>
            </div>
            <div class="font-weight-bold">
                <div class="text-truncate">Tobia Crivellari</div>
                <div class="small text-gray-500">Product Designer at askbootstrap</div>
            </div>
            <span class="ml-auto small">3 hours</span>
        </div>
        <div class="p-3 border-bottom osahan-post-body">
            <p class="mb-0">` + text + `
            </p>
        </div>
        <div class="p-3 border-bottom osahan-post-footer">
            <a class="mr-3 text-secondary  like-button"><i class="feather-heart"></i></a>
            <a href="#" class="mr-3 text-secondary commentButton" onclick="openComment(this)"><i class="feather-message-square"></i></a>
        </div>
    </div>
    `;
    console.log(firstPost);
    firstPost.before(newPost);
    var likeButton = document.querySelector(".like-button");
    // 因为新发的动态永远是第一个 所以只会锁定到它
    likeButton.addEventListener("click", function(event) {
        var heartIcon = likeButton.querySelector(".feather-heart");
        var likeCount = likeButton.querySelector(".like-count");

        if (heartIcon.classList.contains("text-danger")) {
           heartIcon.classList.remove("text-danger");
           var currentCount = parseInt(likeCount.textContent);
           likeCount.textContent = (currentCount - 1).toString();
        } else {
           heartIcon.classList.add("text-danger");
           var currentCount = parseInt(likeCount.textContent);
           likeCount.textContent = (currentCount + 1).toString();
        }
        event.preventDefault(); // 阻止默认链接行为
     });
}

function addComment () {
    if (currentCommentButton) {
		var picid = localStorage.getItem("randompic");
	    var picsrc = "img/p"+picid+".png";
        var commentText = document.getElementById('comment_text').value;
        var newPost = `
        <div class="p-3 d-flex align-items-top border-bottom osahan-post-comment">
            <div class="dropdown-list-image mr-3">
                <img class="rounded-circle" src=`+ picsrc +` alt="">
                <div class="status-indicator bg-success"></div>
            </div>
            <div class="font-weight-bold">
                <div class="text-truncate"> James Spiegel </div>
                <div class="small text-gray-500">` + commentText + `</div>
            </div>
        </div>
        `;
        
        var insertPlace = currentCommentButton.parentElement;
        console.log(document.getElementById('comment_text'));
        console.log(commentText);
        console.log(insertPlace);
        insertPlace.insertAdjacentHTML('afterend', newPost);
        closeComment();
    }
}

// document.querySelectorAll('.commentButton').forEach(function(button) {
//     // 对每一个按钮进行操作
//     // 添加监听器
//     button.addEventListener('click', function() {
//       // 获取帖子的唯一标识符
//       var postId = this.getAttribute('data-postid');
      
//       // 在模态框中显示帖子标识符（用于演示，你可以根据需要进行其他操作）
//       alert('Clicked Comment for Post ID: ' + postId);
  
//       // 显示评论模态框
//       document.getElementById('commentModal').style.display = 'block';
//     });
// });

function openComment (button) {
    currentCommentButton = button;
    var popup = document.getElementById('comment_window');
    popup.style.display = 'block';
}

function closeComment () {
    var popup = document.getElementById('comment_window');
    popup.style.display = 'none';
    popup.querySelector('textarea').value = '';
}
// // 初始化已发送的帖子数组，或者从本地存储中检索
// var savedPosts = JSON.parse(localStorage.getItem('savedPosts')) || [];

// // 当页面加载时，显示已保存的帖子
// function displaySavedPosts() {
//     var postsContainer = $('#myTabContent');

//     savedPosts.forEach(function (post) {
//         postsContainer.append(post);
//     });
// }

// // 当点击 "发送" 按钮时执行操作
// function createNewPost() {
//     // 获取当前文本框的内容
//     var activeTabId = $('#myTab .nav-link.active').attr('href');
//     var inputText = $(activeTabId + ' textarea').val();

//     // 创建一个新的帖子框
//     var newPost = `
//     <div class="box shadow-sm border rounded bg-white mb-3 osahan-post">
//     <!-- 这里放置新帖子的内容 -->
//     </div>
// `;

//     // 插入新帖子框到页面中
//     $('#myTabContent').prepend(newPost);

//     // 保存新帖子到已发送的帖子数组
//     savedPosts.push(newPost);

//     // 清空文本框内容
//     $(activeTabId + ' textarea').val('');

//     // 将已发送的帖子保存到本地存储
//     localStorage.setItem('savedPosts', JSON.stringify(savedPosts));
// }


// // 在页面加载时，显示已保存的帖子
// $(document).ready(function () {
//     displaySavedPosts();
// });
