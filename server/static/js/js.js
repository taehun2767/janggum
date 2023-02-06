const requestComment = new XMLHttpRequest();
const requestDelete = new XMLHttpRequest();
const requestLike = new XMLHttpRequest();


//좋아요
const onClickLike = (id) => {
    const url = '/like_ajax/';
    requestLike.open("POST", url, true);
    requestLike.setRequestHeader(
        "Content-Type",
        "application/x-www-form-urlencoded"
    );
    requestLike.send(JSON.stringify({id: id}));
};

requestLike.onreadystatechange = () => {
    if (requestLike.readyState === XMLHttpRequest.DONE) {
        if (requestLike.status < 400) {
            const {id, liked} = JSON.parse(requestLike.response);
            const element = document.querySelector(`.post_${id} .post_like`);
            const originHTML = element.innerHTML
            console.log(element)
            console.log(originHTML)
            if (liked == true) {
                element.innerHTML = '<i class="fa-solid fa-heart"></i>';
            } else if (liked == false) {
                element.innerHTML = '<i class="fa-regular fa-heart"></i>';
            } else {
                element.innerHTML = '<i class="fa-regular fa-heart"></i>';
            }
        }
    }
};

//댓글 달기
const onClickComment = (id) => {
    const url = '/comment_ajax/';
    content = document.querySelector(`.comment_form_${id}`).value;
    requestComment.open("POST", url, true);
    requestComment.setRequestHeader(
        "content-Type",
        "application/x-www-form-urlencoded"
    );
    requestComment.send(JSON.stringify({id: id, content: content}));
}

requestComment.onreadystatechange = () => {
    if (requestComment.readyState === XMLHttpRequest.DONE){
        if (requestComment.status < 400) {
            const {post_id, comment_id, content} = JSON.parse(requestComment.response);
            const element = document.querySelector(`.comment_list_${post_id}`); //댓글:
            const originHTML = element.innerHTML;
            // const [com, commentContent] = originHTML.split(":")
            // element.innerHTML = `댓글: ${commentContent}`;
            element.innerHTML = originHTML + `<div class="comment_id_${comment_id}">
                            <p>댓글: ${content}</p>
                        <button onclick="onClickDelete(${post_id}, ${comment_id})">삭제</button>
                        <hr>
                    </div>`;
            document.querySelector(`.comment_form_${post_id}`).value = "";
        }
    }
}

//댓글 삭제
const onClickDelete = (post_id, comment_id) => {
    const url = 'comment_del_ajax/';
    requestDelete.open("POST", url, true);
    requestDelete.setRequestHeader(
        "Content-Type",
        "application/x-www-form-urlencoded"
    );
    requestDelete.send(JSON.stringify({post_id: post_id, comment_id: comment_id}));
};

requestDelete.onreadystatechange = () => {
    if (requestDelete.readyState === XMLHttpRequest.DONE) {
        if (requestDelete.status < 400) {
            const { post_id, comment_id } = JSON.parse(requestDelete.response);
            const comment = document.querySelector(`.post_${post_id} .comment_id_${comment_id}`);
            comment.remove();
        }
    }
};
