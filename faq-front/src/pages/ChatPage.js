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
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const apiEndpoint = process.env.REACT_APP_API;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const sendQuery = async () => {
    if (query.trim()) {
      const newMessage = { text: `You: ${query}`, type: "sent" };
      setMessages([...messages, newMessage]);
      setQuery("");

      try {
        const response = await axios.post(
          `${apiEndpoint}/ask`,
          { query },
//          {
//            headers: { Authorization: `Bearer ${apiKey}` },
//          }
        );
        setMessages((messages) => [
          ...messages,
          { text: `Reply: ${response.data}`, type: "received" },
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
          value={query}
          onChange={(e, { value }) => setQuery(value)}
          onKeyPress={(e) => e.key === "Enter" && sendQuery()}
        />
      </Form>
    </Container>
  );
}

export default ChatPage;
