FROM golang:1.21-alpine AS build
WORKDIR /src
COPY . .
RUN go build -o /bin/auth-service main.go

FROM alpine:3.18
COPY --from=build /bin/auth-service /bin/auth-service
EXPOSE 8081
ENTRYPOINT ["/bin/auth-service"]
