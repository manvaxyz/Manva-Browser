FROM golang:1.21-alpine AS build
WORKDIR /src
COPY . .
RUN go build -o /bin/model-registry main.go

FROM alpine:3.18
COPY --from=build /bin/model-registry /bin/model-registry
EXPOSE 8083
ENTRYPOINT ["/bin/model-registry"]
