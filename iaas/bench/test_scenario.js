/**
 * 実際に負荷試験をするテストシナリオである。
 * 各想定クライアント（ユーザ）は以下の挙動をする。
 * 
 * 1. ToDo 一覧を取得(GET/LIST)
 * 2. ToDo を1件作成(POST)
 * 3. 作成したTodoがあることを確認(GET)
 * 4. 作成したTodoを完了へ変更(PUT)
 * 5. 作成したTodoを削除(DELETE)
 * 6. 作成したTodoが削除されていることを確認(GETで404を期待)
 * 
 * それぞれのリクエストが成功したかどうかを、JSONで吐き出す。
 * JSONの形式は https://docs.k6.io/docs/results-output#section-json-output に沿う。
 */

import http from "k6/http";
import { check, group } from "k6";

// Test target URL must be given via environmental variable
let targetUrl = 'https://example.com';
if (__ENV.TARGET_URL) {
  targetUrl = __ENV.TARGET_URL
}

// The id of todo item, and should be incremented each iteration
let todoId;

// This num is used to create different ToDo IDs for each VU
const BASE_NUMBER = 1000;

// Test scenario itself; See the comment at the top to get a grasp of total flow
export default function () {
  if (todoId === undefined) {
    todoId = __VU * BASE_NUMBER + __ITER
  }

  // [1] LIST
  group('list', () => {
    const resList = http.get(`${targetUrl}/tasks`);
    check(resList, {
      "status is 200": r => r.status === 200
    });
  });

  // [2] Post
  group('post', () => {
    const body = {
      item: `Training Preps ${todoId}`
    }
    const resPost = http.post(`${targetUrl}/tasks`, JSON.stringify(body), { headers: { "Content-Type": "application/json" } });
    check(resPost, {
      "status is 200": r => r.status === 200
    });

    try {
      todoId = JSON.parse(resPost.body).id;
    } catch (e) {
      console.error(e);
    }
  });

  // [3] GET the created item
  group('get', () => {
    const resGetBeforeDeletion = http.get(`${targetUrl}/tasks/${todoId}`);
    check(resGetBeforeDeletion, {
      "status is 200": r => r.status === 200
    });
  });

  // [4] PUT
  group('put', () => {
    const body = {
      item: `Training Preps ${todoId}`,
      is_done: true,
    }
    const resPut = http.put(`${targetUrl}/tasks/${todoId}`, JSON.stringify(body), { headers: { "Content-Type": "application/json" } });
    check(resPut, {
      "status is 200": r => r.status === 200
    });
  });

  // [5] DELETE the created item
  group('delete', () => {
    const resDelete = http.del(`${targetUrl}/tasks/${todoId}`);
    check(resDelete, {
      "status is 204": r => r.status === 204
    });
  });


  // [6] Confirm the item was removed
  group('get', () => {
    const resGetAfterDeletion = http.get(`${targetUrl}/tasks/${todoId}`);
    check(resGetAfterDeletion, {
      "status is 404": r => r.status === 404
    });
  })

  // Increment for next test
  todoId++;
};
