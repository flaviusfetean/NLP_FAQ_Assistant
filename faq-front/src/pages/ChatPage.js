import React, { useState, useEffect, useRef } from "react";
import {
  Input,
  Segment,
  Form,
  Header,
  Container,
  List,
} from "semantic-ui-react";
import axios from "axios";
import './ChatPage.css';

function ChatPage() {
  const [apiKey, setApiKey] = useState("");
  const [user_question, setQuery] = useState("");
  const [messages, setMessages] = useState([
    {
        text: "Server: You are currently unauthenticated to the Openai server. This means that the unmatched questions will be processed locally using orca-mini. For forwarding to openai, please introduce your api key in the field above.",
        type: "received"
    }]);
  const messagesEndRef = useRef(null);
  const apiEndpoint = process.env.REACT_APP_API;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const sendApiKey = async () => {
    if (apiKey.trim()) {
      const newMessage = { text: `Sent api key to server`, type: "sent" };
      setMessages([...messages, newMessage]);

      try {
        const response = await axios.post(
          `${apiEndpoint}/set_api_key`,
          { apiKey },
//          {
//            headers: { Authorization: `Bearer ${apiKey}` },
//          }
        );
        setMessages((messages) => [
          ...messages,
          { text: `${response.data}`, type: "received" },
        ]);
      } catch (error) {
        console.error("Error sending message:", error);
        setMessages((messages) => [
          ...messages,
          { text: "Error: Could not get a reply from server.", type: "received" },
        ]);
      }
    }
  };

  const sendQuery = async () => {
    if (user_question.trim()) {
      const newMessage = { text: `You: ${user_question}`, type: "sent" };
      setMessages([...messages, newMessage]);
      setQuery("");

      try {
        const response = await axios.post(
          `${apiEndpoint}/ask-question`,
          { user_question },
//          {
//            headers: { Authorization: `Bearer ${apiKey}` },
//          }
        );
        //let data = JSON.parse(response.data);
        setMessages((messages) => [
          ...messages,
          { text: `${response.data.source}: ${response.data.answer}`, type: "received" },
        ]);
      } catch (error) {
        console.error("Error sending message:", error);
        setMessages((messages) => [
          ...messages,
          { text: "Error: Could not get a reply.", type: "received" },
        ]);
      }
    }
  };

   return (
    <Container>
      <Segment inverted color="#121212" textAlign="center" style={{ marginTop: '10px'}}>
        <Header as="h2">FAQ Assistant</Header>
        <Input
          fluid
          placeholder="Enter API Key..."
          value={apiKey}
          onChange={(e, { value }) => setApiKey(value)}
          onKeyPress={(e) => e.key === "Enter" && sendApiKey()}
          style={{ marginBottom: "10px" }}
        />
      </Segment>
      <div style={{ height: "350px", overflowY: "auto" }}>
        <List relaxed>
          {messages.map((msg, index) => (
            <List.Item
              key={index}
              style={{
                display: "flex",
                justifyContent: msg.type === "sent" ? "flex-end" : "flex-start",
              }}
            >
              <List.Content
                style={{
                  maxWidth: "60%",
                  padding: "5px 10px",
                  borderRadius: "15px",
                  backgroundColor: msg.type === "sent" ? "#f1f1f1" : "#fff5cc",
                  color: msg.type === "sent" ? "black" : "white",
                }}
              >
                <List.Description>{msg.text}</List.Description>
              </List.Content>
            </List.Item>
          ))}
        </List>
      </div>
      <Form>
        <Input
          action={{
            labelPosition: "right",
            icon: "send",
            content: "Send",
            onClick: sendQuery,
            //disabled: !apiKey.trim(),
            className: "customYellowButton"
          }}
          fluid
          placeholder="Type a message..."
          value={user_question}
          onChange={(e, { value }) => setQuery(value)}
          onKeyPress={(e) => e.key === "Enter" && sendQuery()}
        />
      </Form>
    </Container>
  );
}

export default ChatPage;
