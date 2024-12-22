import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import {
  Button,
  Card,
  CardActions,
  CardContent,
  Chip,
  Grid,
  Skeleton,
  Switch,
  TextField,
} from "@mui/material";
import DoneAllIcon from "@mui/icons-material/DoneAll";
import PendingIcon from "@mui/icons-material/Pending";
import EditIcon from "@mui/icons-material/Edit";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import Swal from "sweetalert2";
import { TodoType } from "../../../types/todo";
import {
  createTodo,
  deleteTodo,
  loadTodos,
  updateTodo,
} from "../../../store/services/sliceService";

const initialPost = { title: "", description: "", completed: false };

export default function Latest() {
  const [loadingPost, setLoadingPost] = React.useState<boolean>(true);
  const [tabValue, setTabValue] = React.useState<number>(0);
  const [posts, setPosts] = React.useState<TodoType[]>();
  const [selectedPost, setSelecetedPost] = React.useState<TodoType>();
  const [postObj, setPostObj] = React.useState(initialPost);
  const [postObjErr, setPostObjErr] = React.useState(initialPost);

  const handleClearSelectedPost = () => {
    setSelecetedPost(initialPost);
    setPostObj(initialPost);
    setPostObjErr(initialPost);
    setTabValue(0);
  };

  const handleClick = (value: number) => {
    handleClearSelectedPost();
    setTabValue(value);
  };

  const handleSwitchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPostObj((pre) => ({ ...pre, completed: Boolean(event.target.checked) }));
  };
  const handleLoadPosts = React.useCallback(async () => {
    try {
      setLoadingPost(true);
      const response = await loadTodos();
      console.log("[!] response ", response);
      if (response.status === 200) {
        setPosts(response.data || []);
        return;
      }
      Swal.fire("Failed to load todos");
    } catch (error) {
      console.log("[!] ", error);
      Swal.fire({
        icon: "error",
        title: "Failed to load todos",
      });
      setPosts([]);
    } finally {
      handleClearSelectedPost();
      setLoadingPost(false);
    }
  }, []);

  const handleSubmitPost = React.useCallback(async () => {
    try {
      if (!postObj.title)
        return setPostObjErr((pre) => ({ ...pre, title: "Title is required" }));
      if (!postObj.description)
        return setPostObjErr((pre) => ({
          ...pre,
          tag: "Description is required",
        }));
      if (!postObj.description)
        return setPostObjErr((pre) => ({
          ...pre,
          description: "Description is required",
        }));
      setLoadingPost(true);
      const response = await createTodo({ ...postObj });
      if (response.status === 201) {
        Swal.fire({ icon: "success", title: "Todo created successfully" });
        return;
      }
      Swal.fire("Failed to create ");
    } catch (error) {
      console.log("[!] ", error);
      Swal.fire({ icon: "error", title: "Failed to submit post" });
    } finally {
      handleLoadPosts();
      setLoadingPost(false);
      setTabValue(0);
    }
  }, [handleLoadPosts, postObj]);

  const handleEditPost = React.useCallback(async () => {
    try {
      if (!postObj.title)
        return setPostObjErr((pre) => ({
          ...pre,
          title: "Title is required",
        }));
      if (!postObj.description)
        return setPostObjErr((pre) => ({
          ...pre,
          tag: "Description is required",
        }));
      if (!postObj.description)
        return setPostObjErr((pre) => ({
          ...pre,
          description: "Description is required",
        }));
      await updateTodo({ ...postObj });
    } catch (error) {
      console.log("[!] ", error);
      Swal.fire({ icon: "error", title: "Failed to update post" });
    } finally {
      handleLoadPosts();
      setLoadingPost(false);
      setTabValue(0);
    }
  }, [handleLoadPosts, postObj]);

  const handleDeletePost = React.useCallback(
    async (todoItem: TodoType) => {
      try {
        const response = await deleteTodo(todoItem);
        if (response.status === 204) {
          Swal.fire({
            icon: "success",
            title: "Success",
            text: "Post Deleted",
          });
          handleLoadPosts();
          return;
        }
        Swal.fire("Failed to delete post");
      } catch (error) {
        // eslint-disable-next-line @typescript-eslint/no-unused-expressions
        console.log("[!] "), error;
        Swal.fire({
          icon: "error",
          title: "failed delete post",
        });
      } finally {
        handleLoadPosts();
        setLoadingPost(false);
        setTabValue(0);
      }
    },
    [handleLoadPosts]
  );

  const handleSetToEdit = React.useCallback(
    (postId: string) => {
      const editingPost = posts?.find(
        (item) => item?.id?.toString() === postId
      );
      if (editingPost) {
        setSelecetedPost(editingPost);
        setPostObj({ ...editingPost });
        setTabValue(1);
      }
    },
    [posts]
  );

  const handleSubmitBtnClick = () => {
    if (selectedPost?.id) {
      handleEditPost();
    } else {
      handleSubmitPost();
    }
  };

  React.useEffect(() => {
    handleLoadPosts();
  }, [handleLoadPosts]);

  return (
    <Grid container width="100%">
      <Typography variant="h2" gutterBottom>
        {selectedPost?.id
          ? "Edit Todo"
          : tabValue === 0
          ? "Todo List"
          : "Add Todo"}
      </Typography>
      <Grid item xs={12} mb={1}>
        <Box
          sx={{
            display: "inline-flex",
            flexDirection: "row",
            gap: 3,
            overflow: "auto",
          }}
        >
          <Chip
            onClick={() => handleClick(0)}
            size="medium"
            label="List"
            sx={{
              backgroundColor: tabValue === 0 ? "lightgray" : "transparent",
              border: "1px solid gray",
            }}
          />
          {!selectedPost?.id && (
            <Chip
              onClick={() => handleClick(1)}
              size="medium"
              label="Add"
              sx={{
                backgroundColor: tabValue === 1 ? "lightgray" : "transparent",
                border: "1px solid gray",
              }}
            />
          )}
        </Box>
      </Grid>

      {loadingPost ? (
        <Box display="flex" flexDirection="column" gap={1} width="100%">
          <Skeleton width="100%" />
          <Skeleton width="100%" />
          <Skeleton width="100%" />
        </Box>
      ) : (
        tabValue === 0 && (
          <Grid container gap={1} width="100%">
            {!posts?.length ? (
              <Box>
                <Typography padding={1} variant="h5">
                  No Posts Found
                </Typography>
              </Box>
            ) : (
              posts.map((article, index) => (
                <Box
                  sx={{ minWidth: 275, width: "100%" }}
                  key={`post card ${index}`}
                >
                  <Card variant="outlined">
                    <CardContent
                      sx={{ display: "flex", justifyContent: "space-between" }}
                    >
                      <Box>
                        <Typography variant="h5" component="div">
                          {article.title}
                        </Typography>
                        <Typography variant="body2">
                          {article.description}
                        </Typography>
                      </Box>

                      <Chip
                        icon={
                          article.completed ? (
                            <DoneAllIcon sx={{ color: "white !important" }} />
                          ) : (
                            <PendingIcon sx={{ color: "red !important" }} />
                          )
                        }
                        size="medium"
                        label={article.completed ? "Completed" : "Inprogress"}
                        sx={{
                          color: "white",
                          backgroundColor: article.completed
                            ? "green"
                            : "orange",
                          border: article.completed ? "1px solid gray" : "none",
                        }}
                      />
                    </CardContent>
                    <CardActions>
                      <Box
                        width="100%"
                        display="flex"
                        justifyContent="flex-end"
                        gap={1}
                      >
                        <Button
                          variant="contained"
                          onClick={() => {
                            if (article?.id) {
                              handleSetToEdit(article.id?.toString());
                            }
                          }}
                        >
                          <EditIcon />
                        </Button>
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={() => {
                            if (article?.id) {
                              handleDeletePost(article);
                            }
                          }}
                        >
                          <DeleteOutlineIcon />
                        </Button>
                      </Box>
                    </CardActions>
                  </Card>
                </Box>
              ))
            )}
          </Grid>
        )
      )}
      {tabValue === 1 && (
        <Grid container gap="1em">
          <TextField
            fullWidth
            placeholder="Todo Title"
            size="small"
            value={postObj.title}
            onChange={(e) => {
              setPostObj((pre) => ({ ...pre, title: e.target.value }));
              setPostObjErr((pre) => ({ ...pre, title: "" }));
            }}
            error={postObjErr.title.length > 0}
            helperText={[postObjErr.title]}
          />
          <TextField
            fullWidth
            placeholder="Todo Description"
            size="small"
            value={postObj.description}
            onChange={(e) => {
              setPostObj((pre) => ({ ...pre, description: e.target.value }));
              setPostObjErr((pre) => ({ ...pre, description: "" }));
            }}
            error={postObjErr.description.length > 0}
            helperText={[postObjErr.description]}
          />
          {selectedPost?.id && (
            <Box sx={{ display: "flex", gap: "5px", alignItems: "center" }}>
              <Typography>Status : </Typography>
              <Switch
                checked={postObj.completed}
                color={postObj.completed ? "secondary" : "warning"}
                onChange={handleSwitchChange}
              />
            </Box>
          )}
          <Grid
            item
            xs={12}
            display="flex"
            justifyContent="flex-end"
            gap="10px"
          >
            <Button
              variant="outlined"
              color="error"
              onClick={() => handleClearSelectedPost()}
            >
              Cancel
            </Button>
            <Button variant="contained" onClick={() => handleSubmitBtnClick()}>
              Submit
            </Button>
          </Grid>
        </Grid>
      )}
    </Grid>
  );
}
