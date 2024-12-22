import { TodoType } from "../../types/todo";
import { todoServiceClient } from "../../util/api";

export const loadTodos = async () => {
  const response = await todoServiceClient.get("/todos/");
  return response;
};
export const createTodo = async (item: TodoType) => {
  const response = await todoServiceClient.post("/todos/", item);
  return response;
};
export const updateTodo = async (item: TodoType) => {
  const response = await todoServiceClient .put(`/todos/${item.id}/`, item);
  return response;
};
export const deleteTodo = async (item: TodoType) => {
  const response = await todoServiceClient.delete(`/todos/${item.id}/`);
  return response;
};

